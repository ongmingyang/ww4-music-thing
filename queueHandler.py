import os, random

def randomhash():
  hash = random.getrandbits(32)  
  hash = "%8x" % hash
  return hash

def allowedFile(filename):
  allowed = set(['mp3', 'wav', 'ogg', 'flac', 'm4a'])
  return '.' in filename and \
    filename.rsplit('.', 1)[1] in allowed 

def parseFilename(dump):
  linedump = dump[1]
  filename = linedump[5:]
  return filename

def popFromQueue(mostCurrent):
  try:
    queue = []
    toUnlink = []
    f = open('queue', 'r')
    lines = f.readlines()
    f.close()
    # race conditions possible?
    f = open('queue', 'wb')
    reachedCurrent = False
    for line in lines:    
      # possible namespace conflict, but reduced with random hash w.h.p.
      if line == mostCurrent+'\n':
        reachedCurrent = True
      if reachedCurrent:
        queue.append(line) 
        f.write(line)
      else:
        filename = line[:-1]
        toUnlink.append(filename)
    if reachedCurrent == False:
      queue.append(mostCurrent)
      for line in lines:
        f.write(line)
    else:
      for path in toUnlink:
        print path
        try:
          os.unlink(path)
        except:
          pass
    f.close()
    return queue
  except:
    raise(IOError)

def appendToQueue(filename):
  try:
    f = open('queue', 'a')
    f.write(filename+'\n') 
    f.close()
  except:
    raise(IOError)

def appendAndPop(filename, mostCurrent):
  appendToQueue(filename)
  currentQueue = popFromQueue(mostCurrent)
  return currentQueue
