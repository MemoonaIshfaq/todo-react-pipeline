// src/components/TodoForm.js
import React, { useState, useEffect } from "react";
import { db } from "../firebase";
import { addDoc, collection, getDocs, deleteDoc, doc } from "firebase/firestore";

const TodoForm = () => {
  const [task, setTask] = useState({
    name: "",
    description: "",
    status: "Pending",
    date: "",
  });

  const [taskList, setTaskList] = useState([]);

  const handleChange = (e) => {
    setTask({ ...task, [e.target.name]: e.target.value });
  };

  const handleAddTask = async () => {
    if (!task.name || !task.date) {
      alert("Please fill all required fields");
      return;
    }
    try {
      await addDoc(collection(db, "tasks"), task);
      setTask({ name: "", description: "", status: "Pending", date: "" });
      fetchTasks(); // Reload the task list
    } catch (error) {
      console.error("Error adding task:", error);
    }
  };

  const fetchTasks = async () => {
    const querySnapshot = await getDocs(collection(db, "tasks"));
    const tasksArray = querySnapshot.docs.map((doc) => ({
      id: doc.id,
      ...doc.data(),
    }));
    setTaskList(tasksArray);
  };

  const handleDeleteTask = async (id) => {
    try {
      await deleteDoc(doc(db, "tasks", id));
      fetchTasks();
    } catch (error) {
      console.error("Error deleting task:", error);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  return (
    <div className="max-w-xl mx-auto p-6 bg-purple-100 rounded shadow">
      <h1 className="text-3xl text-purple-700 font-bold mb-6 text-center">📝 My To-Do List</h1>

      <input
        name="name"
        type="text"
        placeholder="Task Name"
        value={task.name}
        onChange={handleChange}
        className="w-full p-2 mb-3 rounded border border-purple-300"
      />
      <textarea
        name="description"
        placeholder="Description"
        value={task.description}
        onChange={handleChange}
        className="w-full p-2 mb-3 rounded border border-purple-300"
      />
      <select
        name="status"
        value={task.status}
        onChange={handleChange}
        className="w-full p-2 mb-3 rounded border border-purple-300"
      >
        <option value="Pending">Pending</option>
        <option value="In Progress">In Progress</option>
        <option value="Completed">Completed</option>
      </select>
      <input
        name="date"
        type="date"
        value={task.date}
        onChange={handleChange}
        className="w-full p-2 mb-3 rounded border border-purple-300"
      />
      <button
        onClick={handleAddTask}
        className="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700"
      >
        Add Task
      </button>

      <div className="mt-6">
        <h2 className="text-xl font-semibold text-purple-700 mb-4">📋 Tasks</h2>
        {taskList.map((t) => (
          <div key={t.id} className="bg-white p-4 rounded mb-3 shadow">
            <h3 className="font-bold">{t.name}</h3>
            <p>{t.description}</p>
            <p>
              <strong>Status:</strong> {t.status}
            </p>
            <p>
              <strong>Date:</strong> {t.date}
            </p>
            <button
              onClick={() => handleDeleteTask(t.id)}
              className="mt-2 bg-red-500 text-white px-2 py-1 rounded hover:bg-red-700"
            >
              Delete
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TodoForm;
