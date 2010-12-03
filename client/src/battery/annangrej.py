#!/usr/bin/python2.5

import osso

def main():
    
    osso_c = osso.Context("osso_test_statusbar", "0.0.1", False)
    
    statusbar = osso.Statusbar(osso_c)

    statusbar.statusbar_send_event("display", 1, 1, "")

if __name__ == "__main__":
    main()
