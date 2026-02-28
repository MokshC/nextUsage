# nextUsage
Keyboard shortcut bindable script for [BlackMagic's DaVinci Resolve](https://www.blackmagicdesign.com/products/davinciresolve/)

## Installing Script
***Note**: Script bindings change based on the page you’re on, there are folders within the scripts dropdown like “Edit”, “Color”, and “Deliver”. When on one of those pages the scripts showing will be from those folders. You can still access them from any page by navigating the drop downs. This is why I place keyboard shortcuts in their own folder unchanged by page changes.*

### Steps
1. In Resolve open the Fusion page, in the toolbar click “Fusion > Fusion Settings”
2. Click “Path Map” in the Fusion drop down of the settings window, and make sure “Scripts” is set to “UserPaths:Scripts”. If not, hit the “Reset” button.
3. Click "Script" in the Fusion drop down of the settings window, change selection from python 2.7 to python 3
   - This step is only Resolve version 18.1.4 or later
4. Hit the save button to update all of your changes
5. [Download this repository's latest release](https://github.com/MokshC/nextUsage/releases)
6. Add it to your scripts path. These paths can also be found by clicking the folder icon at the bottom right of "Path Map" from step 2.
   - **LINUX**: `~/.local/share/DaVinciResolve/Fusion/Scripts/Comp/Keyboard Shortcuts`
     - Hint: if you can’t find .local try hitting Ctrl+H to show hidden folders
   - **WINDOWS**: `C:\Users\{NAME}\AppData\Roaming\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Comp\Keyboard Shortcuts`
     - Hint: if you can’t find AppData try going to View > Hidden items in file explorer and hitting the checkbox 
   - **MAC**: `/Library/Application Support/Blackmagic Design/Fusion/Scripts/Comp/Keyboard Shortcuts`
7. Restart Resolve
8. Now when you go open Resolve and, in the toolbar, click “Workspace > Scripts” several scripts should be available.
9. In "Resolve > Keyboard Shortcuts" assign a shortcut to this script.

## Using the script
### Steps
1. Open a timeline in your resolve project
2. Find a clip in the media pool used in this timeline, click on it so it is selected
3. Activate the script by clicking on it in "Workspace > Scripts" or pressing your keyboard shortcut
4. It will now take you to the next usage after your playhead in the timeline, if there are none after it will take you to the first one.
