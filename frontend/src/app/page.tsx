"use client";

import Loader from "@/components/isLoading";
import { useLogoutMutation, useProfileQuery } from "@/redux/services/authApi";

const ProfilePage = () => {
  const { data, isLoading } = useProfileQuery(undefined);
  const [logout, { isLoading: loggingOut }] = useLogoutMutation();
  console.log(data?.email);

  if (isLoading) return <Loader />;

  const handleLogout = async () => {
    try {
      const res = await logout(undefined).unwrap();
      console.log(res);
      window.location.reload();
    } catch (err) {}
    console.log("Logging out...");
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
      <div className="w-full max-w-sm bg-white rounded-lg shadow-md p-6">
        <div className="flex justify-center mb-4">
          <div className="w-20 h-20 rounded-full bg-indigo-600 flex items-center justify-center text-white text-3xl font-bold">
            {data?.name.charAt(0)}
          </div>
        </div>

        <div className="text-center mb-6">
          <h2 className="text-xl font-semibold text-gray-800">{data?.name}</h2>
          <p className="text-gray-500 text-sm">{data?.email}</p>
        </div>

        <hr className="my-4 text-gray-400" />

        <button
          onClick={handleLogout}
          className="w-full bg-red-500 hover:bg-red-600 text-white font-medium py-2.5 px-4 rounded-lg transition-colors duration-200 cursor-pointer"
        >
          {loggingOut ? "Loading..." : "Logout"}
        </button>
      </div>
    </div>
  );
};

export default ProfilePage;
