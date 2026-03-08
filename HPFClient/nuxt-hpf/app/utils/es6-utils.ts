/* eslint-disable @typescript-eslint/no-explicit-any */
// TODO remplacer par lodash

export function groupBy(list: any, keyGetter: any): Map<any, any> {
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
