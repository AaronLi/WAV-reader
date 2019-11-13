import struct, pyaudio

PLAY_MUSIC = True

f1 = 'New Composition #11.wav'
f2 = 'snippet.wav'
f3 = 'snippet2.wav'
f4 = 'lrStereoTest.wav'
f5 = 'snippet3.wav'

p = pyaudio.PyAudio()

with open(f1, 'rb') as f:
    ckID = f.read(4)
    cksize = int.from_bytes(f.read(4), byteorder='little')
    WAVEID = f.read(4)
    WAVEchunks = ''

    print(ckID, cksize//8, WAVEID)

    ckIDFMT = f.read(4)
    cksizeFMT = int.from_bytes(f.read(4), byteorder='little')
    wFormatTag = int.from_bytes(f.read(2), byteorder='little')
    nChannels = int.from_bytes(f.read(2), byteorder='little')
    nSamplesPerSec = int.from_bytes(f.read(4), byteorder='little')
    nAvgBytesPerSec = int.from_bytes(f.read(4), byteorder='little')
    nBlockAlign = int.from_bytes(f.read(2), byteorder='little')
    wBitsPerSample = int.from_bytes(f.read(2), byteorder='little')
    #cbSize = int.from_bytes(f.read(2), byteorder='little')
    #wValidBitsPerSample = f.read(2)
    #dwChannelMask = f.read(4)
    #SubFormat = f.read(16)
    
    while True:
        newckID = f.read(4)
        newckSize = int.from_bytes(f.read(4), byteorder='little')
        print(newckID, newckSize)
        if newckID == b'data':
            break
        f.read(newckSize)
    
    #print(ckIDFMT, cksizeFMT, wFormatTag, nChannels, nSamplesPerSec, nBlockAlign, wBitsPerSample)
    #print(wBitsPerSample, cksize//8, SubFormat, cksizeFMT)
    numSamples= 0

    stream = p.open(format=pyaudio.paFloat32, channels=2, rate=nSamplesPerSec, output=True)

    leftFile = open('leftChannel.txt', 'wb')
    rightFile = open('rightChannel.txt', 'wb')

    audioData = b''
    
    while numSamples < newckSize//8:
        lChannelBits = f.read(wBitsPerSample//8)#float.from_bytes(f.read(4). byteorder='little')
        rChannelBits = f.read(wBitsPerSample//8)
    
        lChannelFloat = struct.unpack('f', lChannelBits)[0]
        rChannelFloat = struct.unpack('f', rChannelBits)[0]

        leftFile.write(lChannelBits)
        rightFile.write(rChannelBits)

        if PLAY_MUSIC:
            audioData+=lChannelBits
            audioData+=rChannelBits

        
        if numSamples % 1024 == 0 and PLAY_MUSIC:
            stream.write(audioData)
            audioData = b''
        numSamples+=1


    stream.stop_stream()
    stream.close()
    
    leftFile.close()
    rightFile.close()

    
