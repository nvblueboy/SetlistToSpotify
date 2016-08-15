## Some tests to see if it works.

import setlist, time


##Test getting setlists from setlist.fm by looking up the MBID.
artists = ["blink-182","Green Day","Yellowcard","Robert Delong"]

for artist in artists:
    print("\n\n")
    print(artist)
    setlistSongs = setlist.getSetlist(artist)
    attempt_count = 0
    while (setlistSongs == False):
        attempt_count += 1
        setlistSongs = setlist.getSetlist(artist)
        time.sleep(1)
        if attempt_count == 5:
            break;
    if setlistSongs != False:
        for song in setlistSongs:
            print(song)
