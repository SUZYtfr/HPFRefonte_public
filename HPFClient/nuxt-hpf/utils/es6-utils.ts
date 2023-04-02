function groupBy(list: any, keyGetter: any): Map<any, any> {
  const map = new Map();
  list.forEach((item: any) => {
    const key = keyGetter(item);
    const collection = map.get(key);
    if (!collection) {
      map.set(key, [item]);
    } else {
      collection.push(item);
    }
  });
  return map;
}

function debounce(fn: Function, ms = 300): any {
  let timeoutId: ReturnType<typeof setTimeout>;
  return function (this: any, ...args: any[]) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn.apply(this, args), ms);
  };
}

// function throttle(fn: Function, wait: number = 300): any {
//   let inThrottle: boolean,
//     lastFn: ReturnType<typeof setTimeout>,
//     lastTime: number;
//   return function (this: any) {
//     // const context = this;
//     const args = arguments;
//     if (!inThrottle) {
//       fn.apply(this, args);
//       lastTime = Date.now();
//       inThrottle = true;
//     } else {
//       clearTimeout(lastFn);
//       lastFn = setTimeout(() => {
//         if (Date.now() - lastTime >= wait) {
//           fn.apply(this, args);
//           lastTime = Date.now();
//         }
//       }, Math.max(wait - (Date.now() - lastTime), 0));
//     }
//   };
// }

function throttle(callback: Function, wait: number = 300, immediate = false): Function {
  let timeout: (NodeJS.Timeout | null) = null;
  let initialCall = true;

  return function (this: any, ...args: any[]) {
    const callNow = immediate && initialCall;
    const next = (): void => {
      callback.apply(this, args);
      timeout = null;
    };

    if (callNow) {
      initialCall = false;
      next();
    }

    if (!timeout) {
      timeout = setTimeout(next, wait);
    }
  };
}

export { groupBy, debounce, throttle };
