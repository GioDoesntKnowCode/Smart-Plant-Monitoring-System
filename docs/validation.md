# Validation runbook

Work through these in order. Each step has a clear pass/fail. Don't skip — the bench tests are how you find a bad solder joint or a wrongly-polarized pump before you flood your floor.

## 0. Pre-flight

- [ ] Pico W flashed with MicroPython, visible in Thonny.
- [ ] `src/secrets.py` exists with real WiFi + Firebase values. (Confirm `secrets.py` is gitignored.)
- [ ] All `src/*.py` uploaded to the Pico's filesystem root.

## 1. Sensor sanity check

**Goal:** confirm the sensor returns sensible numbers and pick a threshold.

1. In `main.py`, temporarily comment out the WiFi/Firebase/pump calls, leaving only `moisture.read(...)` and a `print`.
2. Set `READ_INTERVAL_SECONDS = 5` in `config.py`.
3. Run and watch the REPL. Record three readings:
   - **Air** (sensor dry, on the table) → `A`
   - **Wet soil** (freshly watered pot) → `W`
   - **Dry soil** (pot that has gone too long without water) → `D`
4. Set `MOISTURE_DRY_THRESHOLD ≈ (W + D) / 2`. Don't pick the air value — air is much drier than even bone-dry soil and will make the threshold useless.

**Pass when:** values are stable (±200 between consecutive reads) and `D < W` clearly.

## 2. Pump bench test

**Goal:** confirm the relay switches and the pump moves water, and calibrate dose duration.

> ⚠️ The kit's pump must be submerged before powering on. Never run it dry — even a few seconds in air can damage it.

1. Pump fully submerged in a cup of water, outlet aimed into a measuring cup.
2. In `main.py`, leave only a `pump.dose(PUMP_PIN, 2)` call.
3. Run. Listen for the relay click on channel 1; watch water move.
4. Measure mL pumped in 2 s. Rated flow is ~28 mL/s, but real-world is usually less because of head height and tube friction. Pick `PUMP_DOSE_SECONDS` so one dose ≈ what your plant wants. Typical small houseplant: 30–60 mL.

**Pass when:** the relay clicks on/off and the pump moves a measurable amount of water in the time you set.

**If the pump runs continuously the moment power is applied** (instead of only during `pump.dose`): the relay is active-low. Set `ACTIVE_HIGH = False` in `src/pump.py` and re-test. Cut power immediately if you see this — sustained dry running kills the pump.

## 3. WiFi + Firebase write

**Goal:** confirm one full reading lands in Firebase.

1. In `main.py`, restore the WiFi connect and `firebase_client.push_reading(...)` calls.
2. Run one cycle.
3. Open the Firebase console → Realtime Database → look for a node `<pi_name>/<timestamp>` with `{ "moisture": <value> }`.

**Pass when:** the node is visible in Firebase and the timestamp is roughly current UTC.

**Common failures:**
- `OSError: -2` from `urequests` → DNS / WiFi not actually up. Add a `print(_wlan.ifconfig())` after connect.
- `401`/`403` from Firebase → wrong DB URL or wrong/expired auth token. Database secrets don't expire; ID tokens do.
- Wrong time (timestamps off by hours/years) → `ntptime.settime()` failed silently. Retry on a fresh boot; default NTP is `pool.ntp.org`.

## 4. End-to-end fast cycle

**Goal:** prove the loop survives multiple iterations and an error mid-cycle doesn't kill the program.

1. Set `READ_INTERVAL_SECONDS = 30`.
2. Set `MOISTURE_DRY_THRESHOLD` artificially high so the pump fires every cycle.
3. Run for ~10 minutes.

**Pass when:** every 30 s you see a Firebase write, and most cycles fire the pump. Yank the WiFi briefly mid-test — the loop should log an error and continue, not crash.

## 5. Production deploy

- Restore `READ_INTERVAL_SECONDS = 4 * 60 * 60`.
- Restore the real `MOISTURE_DRY_THRESHOLD` from step 1.
- Restore the real `PUMP_DOSE_SECONDS` from step 2.
- Mount the Pico somewhere it won't get wet. Route the pump tubing so a stuck-on pump can only flood the pot, not your room.
- Power up. Verify one cycle in Firebase, then leave it.

## Health check after deploy

After 24 hours:
- 6 readings should be in Firebase (one every 4 h).
- The pump should have run only when readings dipped below the threshold.
- The plant should be alive.
