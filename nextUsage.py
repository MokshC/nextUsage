#!/usr/bin/env python

# Created by: Moksh Chitkara
# Last Update: Feb 27th 2026
# v1.0.0
# Copyright (C) 2026  Moksh Chitkara
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# gets current mediapool item
# input: none
# output: mediapool item
def get_media():

    projectManager = resolve.GetProjectManager()
    project = projectManager.GetCurrentProject()
    mediapool = project.GetMediaPool()
    return mediapool.GetSelectedClips()

# Gets current playhead position and converts SMPTE timecode to frame count
# input: timeline [timeline]
# output: frame number [int]
def get_current_frames(timeline):
    
    tc = timeline.GetCurrentTimecode()
    fps = int(timeline.GetSetting("timelineFrameRate"))
    df = bool(int(timeline.GetSetting("timelineDropFrameTimecode")))
    
    if int(tc[9:]) > fps:
	    raise ValueError ('SMPTE timecode to frame rate mismatch.', tc, fps)

    hours   = int(tc[:2])
    minutes = int(tc[3:5])
    seconds = int(tc[6:8])
    frames  = int(tc[9:])

    totalMinutes = int(60 * hours + minutes)

    # Drop frame calculation using the Duncan/Heidelberger method.
    if df:

	    dropFrames = int(round(fps * 0.066666))
	    timeBase   = int(round(fps))

	    hourFrames   = int(timeBase * 60 * 60)
	    minuteFrames = int(timeBase * 60)

	    frm = int(((hourFrames * hours) + (minuteFrames * minutes) + (timeBase * seconds) + frames) - (dropFrames * (totalMinutes - (totalMinutes // 10))))

    # Non drop frame calculation.
    else:

	    fps = int(round(fps))
	    frm = int((totalMinutes * 60 + seconds) * fps + frames)

    return frm

# Converts frame count to SMPTE timecode.
# input: frame [int], timeline
# output: timecode in format "##:##:##:##"
def get_tc(frames, timeline):
        frames = abs(frames)
        fps = int(timeline.GetSetting("timelineFrameRate"))
        df = bool(int(timeline.GetSetting("timelineDropFrameTimecode")))

        # Drop frame calculation using the Duncan/Heidelberger method.
        if df:

	        spacer = ':'
	        spacer2 = ';'

	        dropFrames         = int(round(fps * .066666))
	        framesPerHour      = int(round(fps * 3600))
	        framesPer24Hours   = framesPerHour * 24
	        framesPer10Minutes = int(round(fps * 600))
	        framesPerMinute    = int(round(fps) * 60 - dropFrames)

	        frames = frames % framesPer24Hours

	        d = frames // framesPer10Minutes
	        m = frames % framesPer10Minutes

	        if m > dropFrames:
		        frames = frames + (dropFrames * 9 * d) + dropFrames * ((m - dropFrames) // framesPerMinute)

	        else:
		        frames = frames + dropFrames * 9 * d

	        frRound = int(round(fps))
	        hr = int(frames // frRound // 60 // 60)
	        mn = int((frames // frRound // 60) % 60)
	        sc = int((frames // frRound) % 60)
	        fr = int(frames % frRound)

        # Non drop frame calculation.
        else:

	        fps = int(round(fps))
	        spacer  = ':'
	        spacer2 = spacer

	        frHour = fps * 3600
	        frMin  = fps * 60

	        hr = int(frames // frHour)
	        mn = int((frames - hr * frHour) // frMin)
	        sc = int((frames - hr * frHour - mn * frMin) // fps)
	        fr = int(round(frames -  hr * frHour - mn * frMin - sc * fps))

        # Return SMPTE timecode string.
        return(
		        str(hr).zfill(2) + spacer +
		        str(mn).zfill(2) + spacer +
		        str(sc).zfill(2) + spacer2 +
		        str(fr).zfill(2)
		        )

# get timeline items that correspond to provided media
# input: media [mediapool item]
# output: matchingItems [list of timeline items], timeline [timeline]
def get_items(media):

    projectManager = resolve.GetProjectManager()
    project = projectManager.GetCurrentProject()
    timeline = project.GetCurrentTimeline()
    timelineItems = []
    mediaID = media.GetMediaId()
    
    for i in range(1, timeline.GetTrackCount("video")+1):
        for item in timeline.GetItemListInTrack("video",i):
            if (item.GetMediaPoolItem()) != None and (mediaID == item.GetMediaPoolItem().GetMediaId()):
                timelineItems.append(item)

    return sorted(timelineItems, key=lambda item: item.GetStart()), timeline

# Jump playhead on timeline to next timecode of provided timeline items
# input: timelineItems [list of timeline items], timeline [timeline]
# output: None
def jump_playhead(timelineItems, timeline):

    targetTC = timelineItems[0].GetStart()
    for item in timelineItems:
        if int(get_current_frames(timeline)) < int(item.GetStart()):
            targetTC = item.GetStart()

    targetTC = get_tc(targetTC, timeline)
    while timeline.GetCurrentTimecode() != targetTC:
        timeline.SetCurrentTimecode(targetTC)

def main():

    media = get_media()[0]  # get first of currently selected media items
    if media:
        print("Media collected")
    else:
        return print("No Media Selected")

    timelineItems, timeline = get_items(media)    # get list of corresponding timeline items
    if timelineItems == []:
        return print("No matching timeline items")
    else:
        print("Found", len(timelineItems), "matching use(s)")
    
    jump_playhead(timelineItems, timeline)     # jump to the next timecode usage of the current clip
    print("Playhead moved")

if __name__ == "__main__":
    main()    

