import React, { useState } from "react";
import { useHistory } from "react-router-dom";

const Profile = () => {
  const [userData, setUserData] = useState({
    fullName: "Иван Иванов",
    email: "ivan@example.com",
    phone: "+7 900 123-45-67",
    organization: "Медицинский центр",
    position: "Врач-офтальмолог",
  });

  const history = useHistory();

  const handleEdit = () => {
    history.push("/edit-profile");
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-100">
      <div className="bg-white p-6 rounded-lg shadow-lg w-96">
        <h2 className="text-2xl font-bold mb-4 text-center">Личный кабинет</h2>

        <div className="mb-3">
          <label className="block text-gray-700">ФИО</label>
          <p className="text-gray-900">{userData.fullName}</p>
        </div>

        <div className="mb-3">
          <label className="block text-gray-700">Email</label>
          <p className="text-gray-900">{userData.email}</p>
        </div>

        <div className="mb-3">
          <label className="block text-gray-700">Номер телефона</label>
          <p className="text-gray-900">{userData.phone}</p>
        </div>

        <div className="mb-3">
          <label className="block text-gray-700">Организация</label>
          <p className="text-gray-900">{userData.organization}</p>
        </div>

        <div className="mb-3">
          <label className="block text-gray-700">Должность</label>
          <p className="text-gray-900">{userData.position}</p>
        </div>

        <button
          onClick={handleEdit}
          className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600 transition"
        >
          Изменить данные
        </button>
      </div>
    </div>
  );
};

export default Profile;
