const os = require('os');

const platforms = {
  WINDOWS: 'WINDOWS',
  MAC: 'MAC',
  LINUX: 'LINUX',
  SUN: 'SUN',
  OPENBSD: 'OPENBSD',
  ANDROID: 'ANDROID',
  AIX: 'AIX',
};

const platformsNames = {
  win32: platforms.WINDOWS,
  darwin: platforms.MAC,
  linux: platforms.LINUX,
  sunos: platforms.SUN,
  openbsd: platforms.OPENBSD,
  android: platforms.ANDROID,
  aix: platforms.AIX,
};

const currentPlatform = platformsNames[os.platform()];

const findHandlerOrDefault = (handlerName, dictionary) => {
  const handler = dictionary[handlerName];

  if (handler) {
    return handler;
  }

  if (dictionary.default) {
    return dictionary.default;
  }

  return () => null;
};


DS = '/';
if (currentPlatform == platforms.WINDOWS){
  DS = '\\';
}
console.log(currentPlatform); // => Hi Maciej Cieslar! You are using Mac.