"""
This is a dummy SMTP server for receiving email. Any Email
of any size is accepted and written to a target directory.

Source: http://www.linux-support.com
"""
import smtpd, os, time, asyncore

class mailserver(smtpd.SMTPServer):
    def __init__(self, host='', port=8000, basepath='.maildumpdir'):
        self.basepath = basepath
        smtpd.SMTPServer.__init__(self, (host, port), None)
        print ('Dummy SMTP Server is listening on port', port)

    def process_message(self, peer, mailfrom, rcpttos, data):
        print ('mail from: %s to: %s of %s' %(mailfrom, repr(rcpttos), peer))
        for rcpt in rcpttos:
            rcpt = rcpt.split('@')[0]
            try:
                _mkdir(self.basepath + os.sep + rcpt)
            except OSError:
                pass

            f = file(self.basepath + os.sep + rcpt + os.sep +
                mailfrom + "-[" + str(tuple(peer)) + "]-" + time.strftime('%Y%m%d%H%M%S'), 'w')
            f.write(data + str(tuple(peer)))
            f.close()

def loop ():
    x = mailserver(port=9025)
    try:
        asyncore.loop(timeout=2)
    except KeyboardInterrupt:
        print ('dummy SMTP server halted.')
        x.close()

def _mkdir(newdir):
    if os.path.isdir(newdir):
        pass
    elif os.path.isfile(newdir):
        raise OSError("a file named '%s' already exists" % newdir)
    else:
        head, tail = os.path.split(newdir)
        if head and not os.path.isdir(head):
            _mkdir(head)
        if tail:
            os.mkdir(newdir)


if __name__=='__main__':
    loop()


