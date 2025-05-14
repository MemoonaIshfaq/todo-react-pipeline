// src/firebase.js
import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";

// Your Firebase config
const firebaseConfig = {
  apiKey: "AIzaSyBtzvBE5zIjenATclyYdsMlRK0BvRTi3kQ",
  authDomain: "to-do-list-ad22e.firebaseapp.com",
  projectId: "to-do-list-ad22e",
  storageBucket: "to-do-list-ad22e.firebasestorage.app",
  messagingSenderId: "278742485946",
  appId: "1:278742485946:web:d5150b0f78be9355bf2b83",
  measurementId: "G-SFD7RT34J4"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

export { db };
