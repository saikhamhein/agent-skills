# Review the actual animation

Make the explanation easy to follow before adding polish. Use the consuming project's review records and approval rules.

## Watch the action

Inspect the whole film at normal speed, then scrutinize transitions frame by frame where needed. A contact sheet alone cannot show a one-frame flash, a melted intermediate or exact synchronization. Use both scene samples and dense frames around pose/contact changes. A failed hand action needs a corrected state or transition, not more camera movement.

Check the full action sequence, not only its beginning/end poses. For planned blinks inspect open, closing, closed, opening and open states; confirm that gaze reaches its target and settles without pupil duplication, fur swimming or sticker-border breathing. Inspect every short facial in-between at delivery size. The optical-flow helper’s success is not evidence of compatible anatomy.

Check that gaze, contact and the consequence agree; objects do not duplicate or teleport; ground/contact anchors stay stable; mouths/eyes return to sensible states; and scene cuts preserve the viewer's understanding. Deliberate still holds are valid. Inspect whether the final composition answers the opening question and allows time to attempt the understanding check.

## Check repetition and progression

During whole-film playback, mark any moment that feels like a replay: the same gesture restarting, the same entrance rhythm, identical reaction/cue pairs, or repeated camera moves. Compare the action order as well as individual frames. Confirm that each return adds evidence, a changed condition or a resolved consequence; a changed caption alone is not enough.

Review recurring scientific motion separately from character performance. Do not remove a necessary cycle or distort a model just to make it look different. Check that attention advances from observation to mechanism to consequence, and that a long shot still has a job. Remove decorative repetition before adding more animation. Contact sheets and duplicate-frame statistics cannot judge boredom or normal-speed rhythm; record the scope of playback actually reviewed.

## Read the text

Inspect full-resolution glyph ink and normal-speed playback at a phone-like size. Verify every caption against the approved script, including punctuation, symbols, subscripts, units and Burmese combining marks. Measure visible text rather than assuming the card's height is its font size. Check the longest copy and maximum motion excursions. Rephrase or split before shrinking below the project's size floor.

Check the actual platform overlay separately when available. A caption covered by player controls in a browser screenshot is evidence of that playback state, not proof that the encoded video itself is cropped. Do not claim a phone check or fluent language review that was not performed.

## Inspect the encoded media

```bash
ffprobe -v error -count_frames \
  -show_entries stream=codec_type,codec_name,width,height,pix_fmt,r_frame_rate,avg_frame_rate,nb_read_frames,duration:format=duration \
  -of json final.mp4
ffmpeg -v error -xerror -i final.mp4 -f null -
ffmpeg -n -hide_banner -loglevel error -ss 1.2 -i final.mp4 -frames:v 1 pose-boundary.png
```

Compare measured dimensions, FPS, frame count and duration against the final plan. Inspect extracted images, not just the source PNGs. Check start/end and both sides of every major boundary. For a contact sheet, FFmpeg's `fps`, `scale` and `tile` filters can sample the final MP4; use denser samples separately for risky transitions.

When audio exists, measure loudness/peaks with FFmpeg `ebur128=peak=true` or the project's QC tool and listen through the full encoded mix. Check complete narration, pronunciation, pauses, synchronization, harsh cues and music masking speech. Follow the project's loudness targets; no single number guarantees intelligibility. If audio cannot be heard, report that limitation rather than inferring success from stream metadata.

Keep source claims, model accuracy, language, rights, technical output and owner approval distinct. Save actual findings and the final artifact hash. Do not treat a successful encode, static test fixture, or helper test as a finished educational video. Deliver approved media under the existing project handoff without adding extra gates.
