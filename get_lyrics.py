# Copyright 2023
# Carlneil Domkam, Kunal Menda, Vaibhav Viswanathan

from typing import List
from dataclasses import dataclass
import argparse

import whisper

@dataclass
class LyricSegment:
    """ Segment of OpenAI Whisper output """
    start_s: float
    end_s: float
    text: str

    def __str__(self) -> str:
        """
        String representation.
        
        :return: string representation of lyric segment.
        """
        return "[%.2f, %.2f]: %s"%(self.start_s, self.end_s, self.text)

@dataclass
class LyricChunks:
    """ Output of OpenAI Whisper """
    segments: List[LyricSegment]

    def __str__(self) -> str:
        """
        String representation.
        
        :return: string representation of lyric chunk.
        """ 
        base = ""
        for s in self.segments:
            base += str(s)
            base += "\n"
        return base

def generate_lyric_chunks(audio_filepath: str) -> LyricChunks:
    """ Run OpenAI Whisper on the given audio file """
    model = whisper.load_model("base")
    result = model.transcribe(audio_filepath)
    
    segments = result["segments"]

    whisper_segments = [
        LyricSegment(
            start_s=segment["start"], 
            end_s=segment["end"], 
            text=segment["text"]
        ) for segment in segments]
    
    return LyricChunks(segments=whisper_segments)

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--audio_file',type=str, help='path to audio file')
    args=parser.parse_args()
    audio_file =args.audio_file
    
    chunks=generate_lyric_chunks(audio_filepath=audio_file)
    print(chunks)