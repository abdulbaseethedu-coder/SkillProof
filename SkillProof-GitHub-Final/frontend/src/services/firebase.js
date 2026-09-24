import { initializeApp } from 'firebase/app'
import { getAuth, GoogleAuthProvider, signInWithPopup, signInWithEmailAndPassword, createUserWithEmailAndPassword, signOut } from 'firebase/auth'

const config = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID,
}

export const firebaseConfigured = Object.values(config).every(Boolean)
let auth = null
if (firebaseConfigured) auth = getAuth(initializeApp(config))

export async function googleSignIn() {
  if (!auth) throw new Error('Google sign-in is not configured. Add Firebase values to frontend/.env.')
  return (await signInWithPopup(auth, new GoogleAuthProvider())).user
}
export async function emailSignIn(email, password) {
  if (!auth) throw new Error('Email sign-in is not configured. Add Firebase values to frontend/.env.')
  return (await signInWithEmailAndPassword(auth, email, password)).user
}
export async function emailSignUp(email, password) {
  if (!auth) throw new Error('Email sign-up is not configured. Add Firebase values to frontend/.env.')
  return (await createUserWithEmailAndPassword(auth, email, password)).user
}
export async function logout() { if (auth) await signOut(auth) }
