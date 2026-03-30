# mini-library

A command-line book management system.

## V0 → V1 Changes

### V0
- Only init and add commands were functional
- No loops used

### V1
- All commands implemented (list, borrow, return, delete)
- Book request system added (request, listrequests)
- Borrow duration tracking added (14-day loan period with countdown)
- Genre field added to books and requests
- listgenre command added (filter books by genre, case-insensitive)
- While loops used, no for loops or lists

### V1 Task List
1. Implemented list command (read file line by line with while loop)
2. Implemented borrow and return commands (with 14-day duration tracking)
3. Implemented delete command
4. Implemented request and listrequests commands
5. Added genre field and listgenre command
6. Improved error handling
