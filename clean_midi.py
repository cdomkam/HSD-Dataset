import mido
import argparse
if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--audio_file", required=True, help="path to audio file")
    args=parser.parse_args()
    
    audio_file=args.audio_file
    # Load your MIDI file
    midi_file = mido.MidiFile(audio_file)
    
    merged_midi_file = mido.MidiFile(ticks_per_beat=midi_file.ticks_per_beat)
    
    # Create a new MIDI track to store the merged notes
    merged_track = mido.MidiTrack(ticks_per_beat=midi_file.ticks_per_beat)
    prev=None

    new_note_time=0
    for track in midi_file.tracks:
        for msg in track:
            if msg.type == 'note_on':
                curr_note=msg.note
                curr_time=msg.time
                if prev and curr_note == prev.note:
                    if curr_time==0:
                        new_note_time+=merged_track[-1].time
                        del merged_track[-1]
                        continue
                elif prev and curr_note != prev.note:
                    if merged_track[-1].type!='note_on':
                        merged_track[-1].time+=new_note_time
                        new_note_time=0
            if msg.type == 'note_off':
                prev=msg

            # print(new_note_time)  
           
            merged_track.append(msg.copy())
            # print(merged_track[-1])
            
            if msg.type=='end_of_track':
                if merged_track[-3].note==prev.note:
                    merged_track[-2].time+=new_note_time
                    
                
            # new_note_time=0


            
            
    print(midi_file.tracks)
    print(merged_track)    

    # Create a new MIDI file with the merged track
    merged_midi_file.tracks.append(merged_track)

    # Save the merged MIDI file
    merged_midi_file.save('merged_file.mid')
