import React, { useEffect, useState } from 'react';
import { Flame } from 'lucide-react';

function App() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchEvents = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/events');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setEvents(data);
    } catch (error) {
      console.error('Failed to fetch events:', error);
      setEvents(['🔥 Error loading events. Check the console.']);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEvents();
    const interval = setInterval(fetchEvents, 15000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-red-800 to-yellow-500 flex items-center justify-center p-6">
      <div className="w-full max-w-2xl bg-black/80 backdrop-blur-sm text-white rounded-2xl shadow-2xl border border-orange-500 p-6">
        <div className="flex items-center justify-between mb-4 border-b border-yellow-500 pb-3">
          <h1 className="text-3xl font-extrabold text-yellow-400 tracking-tight flex items-center gap-2">
            <Flame className="text-red-500" />
            Hot Repo Events
          </h1>
          
        </div>

        {loading ? (
          <div className="flex justify-center py-10">
            <div className="w-10 h-10 border-4 border-yellow-300 border-t-orange-500 rounded-full animate-spin"></div>
          </div>
        ) : (
          <ul className="divide-y divide-yellow-800">
            {events.length === 0 ? (
              <li className="py-6 text-center text-yellow-300 flex items-center justify-center gap-2">
                No recent events. Push 🔥 to the repo!
              </li>
            ) : (
              events.map((eventText, index) => (
                <li
                  key={index}
                  className="py-4 px-2 hover:bg-yellow-900/10 rounded-md transition duration-300 border-l-4 border-transparent hover:border-yellow-500"
                >
                  <span className="block text-orange-200">{eventText}</span>
                </li>
              ))
            )}
          </ul>
        )}
      </div>
    </div>
  );
}

export default App;
