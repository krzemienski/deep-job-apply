"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

interface Resume {
  id: string;
  filename: string;
  created_at: string;
}

interface JobApplication {
  id: string;
  job_url: string;
  status: "pending" | "processing" | "succeeded" | "failed";
  created_at: string;
  completed_at?: string;
  error_message?: string;
}

export default function Dashboard() {
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [applications, setApplications] = useState<JobApplication[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");
  const router = useRouter();

  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/login");
      return;
    }

    // Fetch user data
    const fetchData = async () => {
      try {
        // Fetch resumes
        const resumesResponse = await fetch("http://localhost:8000/api/resumes", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!resumesResponse.ok) {
          if (resumesResponse.status === 401) {
            // Unauthorized, redirect to login
            localStorage.removeItem("token");
            router.push("/login");
            return;
          }
          throw new Error("Failed to fetch resumes");
        }

        const resumesData = await resumesResponse.json();
        setResumes(resumesData);

        // Fetch job applications
        const applicationsResponse = await fetch("http://localhost:8000/api/jobs", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!applicationsResponse.ok) {
          throw new Error("Failed to fetch job applications");
        }

        const applicationsData = await applicationsResponse.json();
        setApplications(applicationsData);
      } catch (err) {
        if (err instanceof Error) {
          setError(err.message);
        } else {
          setError("An error occurred while fetching data");
        }
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, [router]);

  const handleLogout = () => {
    localStorage.removeItem("token");
    router.push("/login");
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "succeeded":
        return "bg-green-100 text-green-800";
      case "failed":
        return "bg-red-100 text-red-800";
      case "processing":
        return "bg-blue-100 text-blue-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">Deep Job Apply</h1>
          <div className="flex items-center space-x-4">
            <button
              onClick={handleLogout}
              className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && (
          <div className="bg-red-50 border-l-4 border-red-400 p-4 mb-6">
            <div className="flex">
              <div className="ml-3">
                <p className="text-sm text-red-700">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Resumes Section */}
        <div className="mb-10">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-semibold text-gray-900">Your Résumés</h2>
            <Link
              href="/dashboard/resumes/upload"
              className="px-4 py-2 bg-blue-600 text-white rounded-md text-sm font-medium hover:bg-blue-700"
            >
              Upload New Résumé
            </Link>
          </div>

          {resumes.length === 0 ? (
            <div className="bg-white shadow rounded-lg p-6 text-center">
              <p className="text-gray-500">You haven&apos;t uploaded any résumés yet.</p>
              <Link
                href="/dashboard/resumes/upload"
                className="mt-4 inline-block px-4 py-2 bg-blue-600 text-white rounded-md text-sm font-medium hover:bg-blue-700"
              >
                Upload Your First Résumé
              </Link>
            </div>
          ) : (
            <div className="bg-white shadow overflow-hidden sm:rounded-md">
              <ul className="divide-y divide-gray-200">
                {resumes.map((resume) => (
                  <li key={resume.id}>
                    <div className="px-4 py-4 sm:px-6">
                      <div className="flex items-center justify-between">
                        <p className="text-sm font-medium text-blue-600 truncate">{resume.filename}</p>
                        <div className="ml-2 flex-shrink-0 flex">
                          <p className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                            Active
                          </p>
                        </div>
                      </div>
                      <div className="mt-2 sm:flex sm:justify-between">
                        <div className="sm:flex">
                          <p className="flex items-center text-sm text-gray-500">
                            Uploaded on {new Date(resume.created_at).toLocaleDateString()}
                          </p>
                        </div>
                        <div className="mt-2 flex items-center text-sm text-gray-500 sm:mt-0">
                          <Link
                            href={`/dashboard/resumes/${resume.id}`}
                            className="text-blue-600 hover:text-blue-500"
                          >
                            View Details
                          </Link>
                        </div>
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>

        {/* Job Applications Section */}
        <div>
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-semibold text-gray-900">Job Applications</h2>
            <Link
              href="/dashboard/jobs/new"
              className="px-4 py-2 bg-blue-600 text-white rounded-md text-sm font-medium hover:bg-blue-700"
            >
              Add New Job URL
            </Link>
          </div>

          {applications.length === 0 ? (
            <div className="bg-white shadow rounded-lg p-6 text-center">
              <p className="text-gray-500">You haven&apos;t applied to any jobs yet.</p>
              <Link
                href="/dashboard/jobs/new"
                className="mt-4 inline-block px-4 py-2 bg-blue-600 text-white rounded-md text-sm font-medium hover:bg-blue-700"
              >
                Add Your First Job URL
              </Link>
            </div>
          ) : (
            <div className="bg-white shadow overflow-hidden sm:rounded-md">
              <ul className="divide-y divide-gray-200">
                {applications.map((application) => (
                  <li key={application.id}>
                    <div className="px-4 py-4 sm:px-6">
                      <div className="flex items-center justify-between">
                        <p className="text-sm font-medium text-blue-600 truncate">
                          {application.job_url}
                        </p>
                        <div className="ml-2 flex-shrink-0 flex">
                          <p
                            className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusColor(
                              application.status
                            )}`}
                          >
                            {application.status.charAt(0).toUpperCase() + application.status.slice(1)}
                          </p>
                        </div>
                      </div>
                      <div className="mt-2 sm:flex sm:justify-between">
                        <div className="sm:flex">
                          <p className="flex items-center text-sm text-gray-500">
                            Applied on {new Date(application.created_at).toLocaleDateString()}
                          </p>
                        </div>
                        <div className="mt-2 flex items-center text-sm text-gray-500 sm:mt-0">
                          <Link
                            href={`/dashboard/jobs/${application.id}`}
                            className="text-blue-600 hover:text-blue-500"
                          >
                            View Details
                          </Link>
                        </div>
                      </div>
                      {application.error_message && (
                        <div className="mt-2">
                          <p className="text-sm text-red-600">{application.error_message}</p>
                        </div>
                      )}
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
