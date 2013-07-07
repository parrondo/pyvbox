import time
import os

import virtualbox
from virtualbox import library

"""
Add helper code to the default IGuest class.
"""


# Define some default params for create session 
class IGuest(library.IGuest):
    __doc__ = library.IGuest.__doc__
    def create_session(self, user, password, domain='', session_name='pyvbox',
                        timeout_ms=0):
        session = super(IGuest, self).create_session(user, password, domain,
                                                    session_name)
        if timeout_ms != 0:
            # There is probably a better way to to this?
            if 'win' in self.os_type_id.lower():
                test_file = 'C:\\autoexec.bat'
            else:
                test_file = '/bin/sh'
            while True:
                try:
                    session.file_query_info(test_file)
                except library.VBoxError as err:
                    time.sleep(0.5)
                    timeout_ms -= 500
                    if timeout_ms <= 0:
                        raise
                    continue
                break
        return session
    create_session.__doc__ = library.IGuest.create_session.__doc__

    # Update guest additions helper
    def update_guest_additions(self, source=None, arguments=[], 
                                     flags=[library.AdditionsUpdateFlag.none]):
        if source is None:
            manager = virtualbox.Manager()
            source = os.path.join(manager.bin_path, "VBoxGuestAdditions.iso")
        if not os.path.exists(source):
            raise IOError("ISO path '%s' not found" % source)
        # Interface bug - doesn't seem to actually take "arguments"
        #super(IGuest, self).update_guest_additions(source, arguments, flags)
        p = super(IGuest, self).update_guest_additions(source, flags)
        return p
    update_guest_additions.__doc__ = \
                       library.IGuest.update_guest_additions.__doc__
