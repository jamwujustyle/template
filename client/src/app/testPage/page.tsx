"use client"; // Mark this component as a Client Component

import { useQuery } from "@tanstack/react-query";
import api from "@/utils/api";

type DataResponse = {
  name: string;
  age: number;
  specialty: string;
};
const fetchData = async (): Promise<DataResponse> => {
  console.log("API Base URL:", api.defaults.baseURL); // Log the baseURL
  const response = await api.get("data");
  return response.data;
};

const Page = () => {
  // Updated useQuery syntax: pass an options object
  const { data, error, isLoading } = useQuery<DataResponse, Error>({
    queryKey: ["fetchData"],
    queryFn: fetchData,
  });

  if (isLoading) {
    return <div>Loading..</div>;
  }

  if (error instanceof Error) {
    return <div> Error: {error.message} </div>;
  }

  return (
    <div>
      <h1>data from backend</h1>
      <pre>{JSON.stringify(data, null)}</pre>
    </div>
  );
};

export default Page;
