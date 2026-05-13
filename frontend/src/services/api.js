/**
 * api.js — Central API service layer.
 *
 * All backend calls go through here. Use relative paths so the
 * Vite proxy handles routing to Flask correctly.
 */

// Auth

export async function loginUser({ username, password }) {
  const res = await fetch("/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
    credentials: "include",
  });

  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Login failed");
  return data;
}

export async function registerUser({ username, password, password2 }) {
  const res = await fetch("/auth/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password, password2 }),
    credentials: "include",
  });

  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Registration failed");
  return data;
}

export async function logoutUser() {
  const res = await fetch("/auth/logout", {
    method: "POST",
    credentials: "include",
  });

  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Logout failed");
  return data;
}

// User / Profile

/**
 * Fetch the currently logged-in user.
 * Returns { username, nickname, email, ... } or { username: null } if not logged in.
 */
export async function fetchUser() {
  try {
    const res = await fetch("/api/user", {
      method: "GET",
      credentials: "include",
    });
    return await res.json();
  } catch {
    return { username: null };
  }
}

export async function fetchUserByUsername(username) {
  const res = await fetch(`/api/user/${username}`, {
    method: "GET",
    credentials: "include",
  });

  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "User not found");
  return data;
}

export async function updateProfile({ nickname, email }) {
  const formData = new FormData();
  formData.append("nickname", nickname);
  formData.append("email", email);

  const res = await fetch("/api/update-profile", {
    method: "POST",
    body: formData,
    credentials: "include",
  });

  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Failed to update profile");
  return data;
}

// Gacha

/**
 * Perform a single gacha pull.
 * Returns { skin: { id, name, champion, rarity, image_path }, is_duplicate }
 */
export async function gachaPull() {
  const res = await fetch("/api/gacha/pull", {
    method: "POST",
    credentials: "include",
  });

  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Pull failed");
  return data;
}

// Skins

/**
 * Fetch all available skins from the backend.
 * Expected response: [{ id, name, champion, image_path, rarity }, ...]
 */
export async function fetchSkins() {
  const res = await fetch("/api/skins", { credentials: "include" });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Failed to fetch skins");
  return data;
}

/**
 * Fetch the skins owned by the current user.
 */
export async function fetchUserCollection() {
  const res = await fetch("/api/collection", { credentials: "include" });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Failed to fetch collection");
  return data;
}

// Gold

/**
 * Fetch the current user's gold balance from the database.
 * Returns { gold: number }
 */
export async function fetchGold() {
  const res = await fetch("/api/gold", { credentials: "include" });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Failed to fetch gold");
  return data;
}

/**
 * Add `amount` gold to the current user's balance.
 * Returns { gold: number } with the updated balance.
 */
export async function addGold(amount = 1) {
  const res = await fetch("/api/gold/add", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify({ amount }),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Failed to add gold");
  return data;
}

/**
 * Claim the 5-minute recurring gold bonus.
 * Returns { gold, bonus_awarded } or throws if cooldown hasn't elapsed.
 */
export async function claimGoldBonus() {
  const res = await fetch("/api/gold/bonus", {
    method: "POST",
    credentials: "include",
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Bonus not ready");
  return data;
}

/**
 * Spend `amount` gold from the current user's balance.
 * Returns { gold: number } with the updated balance.
 */
export async function spendGold(amount) {
  const res = await fetch("/api/gold/spend", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify({ amount }),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Failed to spend gold");
  return data;
}

// Display Slots

export async function fetchDisplaySlots() {
  const res = await fetch("/api/display-slots", { credentials: "include" });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Failed to fetch display slots");
  return data; // [{ slot_index, skin }, ...]
}

export async function updateDisplaySlot(slotIndex, skinId) {
  const res = await fetch(`/api/display-slots/${slotIndex}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify({ skin_id: skinId }),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Failed to update slot");
  return data;
}

export async function clearDisplaySlot(slotIndex) {
  const res = await fetch(`/api/display-slots/${slotIndex}`, {
    method: "DELETE",
    credentials: "include",
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Failed to clear slot");
  return data;
}

export async function unlockSkin(collectionId) {
  const res = await fetch(`/api/collection/unlock/${collectionId}`, {
    method: "POST",
    credentials: "include",
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Failed to unlock skin");
  return data;
}

export async function fetchGachaStatus() {
  const res = await fetch("/api/gacha/status", { credentials: "include" });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Failed to fetch gacha status");
  return data;
}

/**
 * Fetch paginated pull history for the current user.
 * @param {number} page     - 1-based page number
 * @param {number} pageSize - rows per page (default 5)
 * Returns { pulls, total, page, page_size, total_pages }
 */
export async function fetchPullHistory(page = 1, pageSize = 5) {
  const res = await fetch(`/api/gacha/history?page=${page}&page_size=${pageSize}`, {
    credentials: "include",
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Failed to fetch pull history");
  return data;
}