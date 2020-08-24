import { writable } from "svelte/store";

export const sidebarOpen = writable(false);
export const dropdownOpen = writable(false);
export const currentPage = writable("index");
