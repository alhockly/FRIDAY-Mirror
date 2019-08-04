try:
	import snowboydecoder
except Exception:
	pass
import pyaudio
import wave
import simpleaudio as sa
import speech_recognition as speech_rec

detector=None

class Aud():
	def detected_callback(self):
		global audresp,detector
		detector.terminate()
		inconvo = True
		r = speech_rec.Recognizer()
		with speech_rec.Microphone() as source:
			print("Listening")
			#eel.showlistening()
			audio = r.listen(source)

		# recognize speech using Google Speech Recognition
		try:
			# for testing purposes, we're just using the default API key
			# to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
			# instead of `r.recognize_google(audio)`
			speech = r.recognize_google(audio)
			print("\"" + speech + "\"")
			#audresp.speechtext = speech
			#self.handleinput()

		except speech_rec.UnknownValueError:
			print("Google Speech Recognition could not understand audio")
			inconvo = False
			#eel.stoplistening()
			#eel.yousaid("Couldnt understand audio")
		except speech_rec.RequestError as e:
			print("Could not request results from Google Speech Recognition service; {0}".format(e))
			inconvo = False

		detector.start(Aud().detected_callback)

try:
	detector = snowboydecoder.HotwordDetector("Friday.pmdl", sensitivity=0.5, audio_gain=1)
	detector.start(Aud().detected_callback)
except Exception:
	pass