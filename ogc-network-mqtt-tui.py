import sys, os
import curses
import ogc_python_tools.ogc_python_logging as l

MAJOR = 0
MINOR = 1
PATCH = 0

DEFAULT_LOGGING_STATE = l.TRACE

COLOR_FORGROUND = 1
COLOR_FOREGROUND_WINDOW = curses.COLOR_RED
COLOR_BACKGROUND_WINDOW = curses.COLOR_BLACK
COLOR_TEXT = 2
COLOR_FOREGROUND_TEXT   = curses.COLOR_WHITE
COLOR_BACKGROUND_TEXT   = curses.COLOR_BLACK
COLOR_STATUS = 3
COLOR_FOREGROUND_STATUS = curses.COLOR_BLACK
COLOR_BACKGROUND_STATUS = curses.COLOR_WHITE

class base_window:
    app_active = True

    input_key = 0
    screen = 0

    MIN_HEIGHT = 25
    MIN_WIDTH = 80
    screen_height = 0
    screen_width = 0

    cursor_position_y = 0
    cursor_position_x = 0

def process_cursor_movement( key ):
    # move cursor
    if ( key == curses.KEY_DOWN ):
        base_window.cursor_position_y = base_window.cursor_position_y + 1
    elif ( key == curses.KEY_UP ):
        base_window.cursor_position_y = base_window.cursor_position_y - 1
    elif ( key == curses.KEY_RIGHT ):
        base_window.cursor_position_x = base_window.cursor_position_x + 1
    elif ( key == curses.KEY_LEFT ):
        base_window.cursor_position_x = base_window.cursor_position_x - 1

    # check limits
    base_window.cursor_position_y = max( 0, base_window.cursor_position_y )
    base_window.cursor_position_y = min( ( base_window.screen_height - 1 ), base_window.cursor_position_y )
    base_window.cursor_position_x = max( 0, base_window.cursor_position_x )
    base_window.cursor_position_x = min( ( base_window.screen_width - 1 ), base_window.cursor_position_x )
    base_window.screen.move( base_window.cursor_position_y, base_window.cursor_position_x )

def update_status_bar():
    status_bar_string = "Press 'q' to quit | Input: (0x%02X), Cursor Pos: %u, %u" % ( base_window.input_key, base_window.cursor_position_y, base_window.cursor_position_x )
    base_window.screen.attron( curses.color_pair( COLOR_STATUS ) )
    base_window.screen.addstr( ( base_window.screen_height - 1 ), 0, status_bar_string[ :( base_window.screen_width - 1 ) ] )
    base_window.screen.addstr( ( base_window.screen_height - 1 ), len( status_bar_string ), ( " " * ( base_window.screen_width - len( status_bar_string ) - 1 ) ) )
    base_window.screen.attroff( curses.color_pair( COLOR_STATUS ) )

def tui_state_machine( base_screen ):
    base_window.screen = base_screen
    # clear the screen
    base_window.screen.clear()
    base_window.screen.refresh()

    # setup some basic colors
    curses.start_color()
    curses.init_pair( COLOR_FORGROUND, COLOR_FOREGROUND_WINDOW, COLOR_BACKGROUND_WINDOW )
    curses.init_pair( COLOR_TEXT, COLOR_FOREGROUND_TEXT, COLOR_BACKGROUND_TEXT )
    curses.init_pair( COLOR_STATUS, COLOR_FOREGROUND_STATUS, COLOR_BACKGROUND_STATUS )

    # Title screen
    ( base_window.screen_height, base_window.screen_width ) = base_window.screen.getmaxyx()
    string_title = "OGC.Engineering - ogc-network-mqtt-tui"
    string_subtitle = "A Textual User Interface for MQTT on the OGC Network"
    string_version = "V: %s.%s.%s" % ( MAJOR, MINOR, PATCH )
    string_contact = "developer contact - dustin ( at ) ogc.engineering"
    string_start = "Press any key to start"

    start_pos_y = int( ( base_window.screen_height // 2 ) - 2 )
    start_pos_x_title = int( ( base_window.screen_width // 2 ) - ( len( string_title ) // 2 ) - ( len( string_title ) % 2 ) )
    start_pos_x_subtitle = int( ( base_window.screen_width // 2 ) - ( len( string_subtitle ) // 2 ) - ( len( string_subtitle ) % 2 ) )
    start_pos_x_version = int( ( base_window.screen_width // 2 ) - ( len( string_version ) // 2 ) - ( len( string_version ) % 2 ) )
    start_pos_x_contact = int( ( base_window.screen_width // 2 ) - ( len( string_contact ) // 2 ) - ( len( string_contact ) % 2 ) )
    start_pos_x_start = int( ( base_window.screen_width // 2 ) - ( len( string_start ) // 2 ) - ( len( string_start ) % 2 ) )

    base_window.screen.attron( curses.color_pair( COLOR_TEXT ) )
    base_window.screen.attron( curses.A_BOLD )
    base_window.screen.addstr( start_pos_y, start_pos_x_title, string_title )
    base_window.screen.addstr( ( start_pos_y + 1 ), start_pos_x_subtitle, string_subtitle )
    base_window.screen.attroff( curses.A_BOLD )
    base_window.screen.addstr( ( start_pos_y + 2 ), start_pos_x_version, string_version )
    base_window.screen.attron( curses.A_DIM )
    base_window.screen.addstr( ( start_pos_y + 3 ), start_pos_x_contact, string_contact )
    base_window.screen.attroff( curses.A_DIM )
    base_window.screen.addstr( ( start_pos_y + 5 ), start_pos_x_start, string_start )
    base_window.screen.attroff( curses.color_pair( COLOR_TEXT ) )


    # drive the state machine by user input
    base_window.app_active = True
    while( base_window.app_active == True ):
        base_window.input_key = base_window.screen.getch()
        l.log( l.TRACE, "New user input: (0x%02X)" % ( base_window.input_key ) )
        base_window.screen.clear()
        ( base_window.screen_height, base_window.screen_width ) = base_window.screen.getmaxyx()
        l.log( l.TRACE, "Screen size calculated as: %u height, %u width" % ( base_window.screen_height, base_window.screen_width ) )
        if ( base_window.input_key != ord( 'q' ) ):
            # Process key presses by state of machine
            process_cursor_movement( base_window.input_key )
            if ( ( base_window.screen_height >= base_window.MIN_HEIGHT ) and ( base_window.screen_width >= base_window.MIN_WIDTH ) ):
                update_status_bar()
            else:
                warning_screen_size_string = "Screen size reduced below minimum requirements, please increase window size"
                l.log( l.WARNING, "%s" % ( warning_screen_size_string ) )
                base_window.screen.addstr( 0, 0, warning_screen_size_string[ :( base_window.screen_width - 1 ) ] )
        else:
            l.log( l.DEBUG, "Cleanup" )
            base_window.app_active = False
        base_window.screen.refresh()

if __name__ == "__main__":
    # setup logging
    l.threshold_set( DEFAULT_LOGGING_STATE ) # set logging threashold to some default state
    l.storage_use_set( True ) # set storage buffer for use in TUI
    l.log_file_set( "ogc-network-mqtt-tui.log" ) # create a file to save logs

    l.log( l.INFO, "OGC.Engineering - ogc-network-mqtt-tui started" )
    curses.wrapper( tui_state_machine ) # build up and tear down curses interface
    l.log( l.INFO, "OGC.Engineering - ogc-network-mqtt-tui ended" )
