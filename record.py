import argparse
import tempfile
import queue
import sys
import sounddevice as sd
import soundfile as sf 
import numpy 
import os

# Recording functions
def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def rec_and_save():
	parser = argparse.ArgumentParser(add_help=False)
	parser.add_argument(
	    '-l', '--list-devices', action='store_true',
	    help='show list of audio devices and exit')
	args, remaining = parser.parse_known_args()
	if args.list_devices:
	    print(sd.query_devices())
	    parser.exit(0)
	parser = argparse.ArgumentParser(
	    description=__doc__,
	    formatter_class=argparse.RawDescriptionHelpFormatter,
	    parents=[parser])
	parser.add_argument(
	    'filename', nargs='?', metavar='FILENAME',
	    help='audio file to store recording to')
	parser.add_argument(
	    '-d', '--device', type=int_or_str,
	    help='input device (numeric ID or substring)')
	parser.add_argument(
	    '-r', '--samplerate', type=int, help='sampling rate')
	parser.add_argument(
	    '-c', '--channels', type=int, default=1, help='number of input channels')
	parser.add_argument(
	    '-t', '--subtype', type=str, help='sound file subtype (e.g. "PCM_24")')
	args = parser.parse_args(remaining)

	q = queue.Queue()

	def callback(indata, frames, time, status):
	    if status:
	        print(status, file=sys.stderr)
	    q.put(indata.copy())


	try:
	    if args.samplerate is None:
	        device_info = sd.query_devices(args.device, 'input')
	        # soundfile expects an int, sounddevice provides a float:
	        args.samplerate = int(device_info['default_samplerate'])
	    if args.filename is None:
		    args.filename = os.path.join('audio', 'recording.wav')

	    # Make sure the file is opened before recording anything:
	    with sf.SoundFile(args.filename, mode='w', samplerate=args.samplerate,
	                      channels=args.channels, subtype=args.subtype) as file:
	        with sd.InputStream(samplerate=args.samplerate, device=args.device,
	                            channels=args.channels, callback=callback):
	            print('#' * 80)
	            print('press Ctrl+C to stop the recording')
	            print('#' * 80)
	            while True:
	                file.write(q.get())
	except KeyboardInterrupt:
	    print('\nRecording finished: ' + repr(args.filename))
	except Exception as e:
	    parser.exit(type(e).__name__ + ': ' + str(e))
      