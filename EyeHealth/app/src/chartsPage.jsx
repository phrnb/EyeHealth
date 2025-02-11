import React from "react";
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

const data = [
  { day: "01", value: 10 },
  { day: "02", value: 12 },
  { day: "03", value: 8 },
  { day: "04", value: 15 },
  { day: "05", value: 7 },
  { day: "06", value: 18 },
  { day: "07", value: 9 },
  { day: "08", value: 10 },
  { day: "09", value: 5 },
  { day: "10", value: 6 },
  { day: "11", value: 8 },
  { day: "12", value: 10 },
];

const Dashboard = () => {
  return (
    <div className="flex min-h-screen bg-gray-100">
      {/* Sidebar */}
      <div className="w-1/5 bg-white p-6 shadow-md">
        <h2 className="text-lg font-bold mb-4">Eye Health Assistant</h2>
        <nav className="space-y-4">
          <a href="#" className="block text-blue-600 font-semibold">Личный кабинет</a>
          <a href="#" className="block">Статистика пользователей</a>
          <a href="#" className="block font-semibold">Статистика по нейросети</a>
          <a href="#" className="block">Статистика по заболеваниям</a>
          <a href="#" className="block">Менеджмент</a>
          <a href="#" className="block">Администрирование</a>
          <a href="#" className="block text-red-500">Выйти</a>
        </nav>
      </div>

      {/* Main Content */}
      <div className="flex-1 p-10">
        <h1 className="text-2xl font-bold text-gray-800">Статистика по использованию нейросети</h1>
        <p className="text-gray-500 italic">Добро пожаловать, с возвращением к работе!</p>

        <div className="grid grid-cols-3 gap-6 mt-6">
          {/* Общая статистика */}
          <div className="bg-white p-6 rounded-xl shadow-md">
            <h3 className="text-gray-600">Количество хранимых фотографий в базе</h3>
            <p className="text-4xl font-bold text-blue-600 mt-2">33</p>
          </div>

          <div className="bg-white p-6 rounded-xl shadow-md">
            <h3 className="text-gray-600">Количество загруженных снимков (24 часа)</h3>
            <p className="text-4xl font-bold text-black mt-2">14</p>
          </div>

          <div className="bg-white p-6 rounded-xl shadow-md">
            <h3 className="text-gray-600">Количество загруженных снимков (неделя)</h3>
            <p className="text-4xl font-bold text-orange-600 mt-2">19</p>
          </div>

          <div className="bg-white p-6 rounded-xl shadow-md col-span-3">
            <h3 className="text-gray-600">Количество загруженных снимков (месяц)</h3>
            <p className="text-4xl font-bold text-blue-600 mt-2">33</p>
          </div>
        </div>

        {/* График */}
        <div className="bg-white p-6 mt-6 rounded-xl shadow-md">
          <h3 className="text-gray-600 mb-4">Среднее время анализа фотографий</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={data}>
              <XAxis dataKey="day" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#4F46E5" />
            </BarChart>
          </ResponsiveContainer>

          <ResponsiveContainer width="100%" height={150}>
            <LineChart data={data}>
              <XAxis dataKey="day" />
              <YAxis hide />
              <Tooltip />
              <Line type="monotone" dataKey="value" stroke="#E57373" strokeWidth={3} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
