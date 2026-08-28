# RakshaGrid Field — Mobile App for Volunteers

Not yet tested on a device/emulator — Flutter SDK wasn't available in
the build environment. Code follows standard Flutter patterns; verify
it compiles and runs before relying on it.

## Setup
1. Install Flutter SDK: https://docs.flutter.dev/get-started/install
2. `flutter pub get`
3. Edit `lib/services/api_service.dart` — point `baseUrl` at your backend:
   - Android emulator: `http://10.0.2.2:8000` (default, already set)
   - iOS simulator: `http://localhost:8000`
   - Physical phone: your computer's LAN IP, e.g. `http://192.168.1.42:8000`
4. Make sure the backend is running and reachable.
5. `flutter run`

## What it does
- Mission list — fetches `/api/zones/`, sorted by severity
- Zone detail — fetches `/api/demand/{id}`, shows a supply manifest
- Check-in button — UI only, not wired to a backend endpoint yet

## Known gaps
- No login/authentication
- No offline support
- Check-in doesn't persist
- Not tested on a real device or emulator
