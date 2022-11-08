## Dependencies ##
Python:
* eel
* tkinter
* pykakasi (for furigana)

Installed:
* Chrome
* mpv

## GUI controls ##
Assuming default mpv key configuration:

| Button | Function |
| --- | --- |
| S(-1) | Seeks video to the start of the previous subtitle line. |
| S(0) | Seeks video to the start of the current subtitle line. |
| S(1) | Seeks video to the start of the next subtitle line. |
| <- | Seeks video x time back (left key). |
| ▶⏸ | Pauses/resumes the video playback (space key). |
| -> | Seeks video x time forward (right key). |
| TL | Toggles drawing of secondary subtitle track (id=1). |
| Furi | Toggles drawing of furigana (may not be accurate). |
| Wide | Toggles replacing half-width kana with full width kana. If not active, characters will occasionally repeat when furigana is turned on. |
| Vol- | Decreases audio volume (9 key). |
| Vol+ | Increases audio volume (0 key). |
| Sub | Changes subtitle track (j key). |
| Hook | Starts IPC communication with mpv if mpv started with --input-ipc-server. The name of the IPC server must be "\\.\pipe\mpvsocket" for Windows or "/tmp/mpvsocket" for Linux.|
| Open | Asks for video and subtitles files and plays them with mpv. |
| Close | Closes mpv (q key). |

## Keyboard controls ##

Default mpv keys. These are passed to mpv as is:

| Key | Default mpv function |
| --- | --- |
| Space | Pauses video playback. |
| Right | Seeks video x time forward. |
| Left | Seeks video x time back. |
| 0 | Increases audio volume. |
| 9 | Decreases audio volume. |
| q | Closes mpv. |
| j | Changes subtitle track. |

Custom keys:
| Key | Function |
| --- | --- |
| + | Increase font size of browser subtitles by 2px. |
| - | Decrease font size of browser subtitles by 2px. |

## Known issues ##
* Furigana is broken for words starting with kanji that read with repeated kana. For example: 言いそびれる or 叩く.