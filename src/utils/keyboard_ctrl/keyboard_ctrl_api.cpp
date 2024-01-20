#include <windows.h>
#include <iostream>
#include <cstdlib>

void pressAndReleaseKey(WORD key, DWORD durationMs) {
    INPUT input[2];
    input[0].type = INPUT_KEYBOARD;
    input[0].ki.wVk = key;

    input[1].type = INPUT_KEYBOARD;
    input[1].ki.wVk = key;
    input[1].ki.dwFlags = KEYEVENTF_KEYUP;

    SendInput(2, input, sizeof(INPUT));
    Sleep(durationMs);
}

int main(int argc, char *argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << " <key> <duration>\n";
        return 1;
    }

    WORD key = atoi(argv[1]);       // Convert the first argument to key code
    DWORD duration = atoi(argv[2]);  // Convert the second argument to duration

    pressAndReleaseKey(key, duration);

    return 0;
}
