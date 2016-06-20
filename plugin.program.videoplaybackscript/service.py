import os
import pipes
import shlex
import subprocess
import threading
import xbmc
import xbmcaddon


class ListeningPlayer(xbmc.Player):

    def __init__(self):
        xbmc.Player.__init__(self)
        self.isVideo = None
        self.isVideoGuard = threading.Lock()
        self.startScriptEnabled = xbmcaddon.Addon().getSetting('startScriptEnabled')
        self.startScriptPath = xbmcaddon.Addon().getSetting('startScriptPath')
        self.startScriptArgs = xbmcaddon.Addon().getSetting('startScriptArgs')
        self.stopScriptEnabled = xbmcaddon.Addon().getSetting('stopScriptEnabled')
        self.stopScriptPath = xbmcaddon.Addon().getSetting('stopScriptPath')
        self.stopScriptArgs = xbmcaddon.Addon().getSetting('stopScriptArgs')

    def onPlayBackStarted(self):
        isVideo = self.isPlayingVideo()
        with self.isVideoGuard:
            self.isVideo = isVideo
        if (isVideo and
                self.startScriptEnabled and
                os.path.isfile(self.startScriptPath)):
            startScriptCmd = [self.startScriptPath] + shlex.split(self.startScriptArgs)
            xbmc.log(
                    'Video starting triggered script: ' +
                            ' '.join(pipes.quote(arg) for arg in startScriptCmd),
                    xbmc.LOGINFO)
            try:
                subprocess.check_call(startScriptCmd)
            except subprocess.CalledProcessError as e:
                xbmc.log('Video start script failed: ' + str(e))

    def onPlayBackStopped(self):
        with self.isVideoGuard:
            wasVideo = self.isVideo
            self.isVideo = None
        if (wasVideo and
                self.stopScriptEnabled and
                os.path.isfile(self.stopScriptPath)):
            stopScriptCmd = [self.stopScriptPath] + shlex.split(self.stopScriptArgs)
            xbmc.log(
                    'Video stopping triggered script: ' +
                            ' '.join(pipes.quote(arg) for arg in stopScriptCmd),
                    xbmc.LOGINFO)
            try:
                subprocess.check_call(stopScriptCmd)
            except subprocess.CalledProcessError as e:
                xbmc.log('Video stop script failed: ' + str(e))


def main():
    playback = ListeningPlayer()
    xbmc.Monitor().waitForAbort()


if __name__ == "__main__":
    main()
