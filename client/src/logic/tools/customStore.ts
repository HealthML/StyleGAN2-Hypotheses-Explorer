import { Writable as _Writable, writable } from "svelte/store";

declare type Subscriber<T> = (value: T) => void;
declare type Unsubscriber = () => void;
declare type Updater<T> = (value: T) => T;
declare type Invalidator<T> = (value?: T) => void;

/**
 * Adds a @function set method to the store contract
 */
export class Writable<T> implements _Writable<T> {
  private writable: _Writable<T>;
  private value: T;
  constructor(initial: T) {
    this.value = initial;
    this.writable = writable<T>(initial);
    this.writable.subscribe((value) => (this.value = value));
  }

  get() {
    return this.value;
  }

  set(value: T) {
    this.writable.set(value);
  }

  update(updater: Updater<T>): void {
    this.writable.update(updater);
  }

  subscribe(run: Subscriber<T>, invalidate?: Invalidator<T>): Unsubscriber {
    return this.writable.subscribe(run, invalidate);
  }
  subscribe_only_changes(run: Subscriber<T>) {
    let first = true;
    const unsubscribe = this.subscribe((...args) => {
      if (!first) {
        run(...args);
      }
    });
    first = false;
    return unsubscribe;
  }
}
