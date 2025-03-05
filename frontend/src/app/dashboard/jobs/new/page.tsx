"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

interface Resume {
  id: string;
  filename: string;
  created_at: string;
}

export default function AddJobUrl() {
  const [jobUrl, setJobUrl] = useState("");
  const [selectedResumeId, setSelectedResumeId] = useState("");
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/login");
      return;
    }

    // Fetch resumes
    const fetchResumes = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/resumes", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          if (response.status === 401) {
            // Unauthorized, redirect to login
            localStorage.removeItem("token");
            router.push("/login");
            return;
          }
          throw new Error("Failed to fetch resumes");
        }

        const data = await response.json();
        setResumes(data);

        // Auto-select the first resume if available
        if (data.length > 0) {
          setSelectedResumeId(data[0].id);
        }
      } catch (err) {
        if (err instanceof Error) {
          setError(err.message);
        } else {
          setError("An error occurred while fetching resumes");
        }
      } finally {
        setIsLoading(false);
      }
    };

    fetchResumes();
  }, [router]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    // Validate URL
    try {
      new URL(jobUrl);
    } catch {
      setError("Please enter a valid URL");
      return;
    }

    // Validate resume selection
    if (!selectedResumeId) {
      setError("Please select a resume");
      return;
    }

    setIsSubmitting(true);

    try {
      // Get token from localStorage
      const token = localStorage.getItem("token");
      if (!token) {
        router.push("/login");
        return;
      }

      // Submit job URL
      const response = await fetch("http://localhost:8000/api/jobs", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          resume_id: selectedResumeId,
          job_url: jobUrl,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to add job URL");
      }

      // Redirect to dashboard
      router.push("/dashboard");
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("An error occurred while adding the job URL");
      }
      setIsSubmitting(false);
    }
  };

  const handleBulkUpload = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const urls = e.target.value.split("\n").filter(url => url.trim() !== "");
    if (urls.length > 0) {
      setJobUrl(urls[0]);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">Add Job URL</h1>
          <Link
            href="/dashboard"
            className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
          >
            Back to Dashboard
          </Link>
        </div>
      </header>

      <main className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {resumes.length === 0 ? (
          <div className="bg-white shadow sm:rounded-lg p-6 text-center">
            <h2 className="text-lg font-medium text-gray-900 mb-4">No Résumés Available</h2>
            <p className="text-gray-500 mb-6">
              You need to upload a résumé before you can add job URLs.
            </p>
            <Link
              href="/dashboard/resumes/upload"
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700"
            >
              Upload a Résumé
            </Link>
          </div>
        ) : (
          <div className="bg-white shadow sm:rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <h2 className="text-lg leading-6 font-medium text-gray-900">Add a Job URL</h2>
              <div className="mt-2 max-w-xl text-sm text-gray-500">
                <p>
                  Enter the URL of a job listing you want to apply to. Our system will automatically navigate to the page and submit your application.
                </p>
              </div>

              {error && (
                <div className="mt-4 bg-red-50 border-l-4 border-red-400 p-4">
                  <div className="flex">
                    <div className="ml-3">
                      <p className="text-sm text-red-700">{error}</p>
                    </div>
                  </div>
                </div>
              )}

              <form onSubmit={handleSubmit} className="mt-5 space-y-6">
                <div>
                  <label htmlFor="job-url" className="block text-sm font-medium text-gray-700">
                    Job URL
                  </label>
                  <div className="mt-1">
                    <input
                      type="text"
                      name="job-url"
                      id="job-url"
                      className="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                      placeholder="https://example.com/job-listing"
                      value={jobUrl}
                      onChange={(e) => setJobUrl(e.target.value)}
                      required
                    />
                  </div>
                  <p className="mt-2 text-sm text-gray-500">
                    Enter the full URL of the job listing page.
                  </p>
                </div>

                <div>
                  <label htmlFor="resume" className="block text-sm font-medium text-gray-700">
                    Select Résumé
                  </label>
                  <select
                    id="resume"
                    name="resume"
                    className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
                    value={selectedResumeId}
                    onChange={(e) => setSelectedResumeId(e.target.value)}
                    required
                  >
                    {resumes.map((resume) => (
                      <option key={resume.id} value={resume.id}>
                        {resume.filename}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label htmlFor="bulk-urls" className="block text-sm font-medium text-gray-700">
                    Bulk Upload (Optional)
                  </label>
                  <div className="mt-1">
                    <textarea
                      id="bulk-urls"
                      name="bulk-urls"
                      rows={4}
                      className="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                      placeholder="Enter multiple URLs, one per line. Only the first URL will be processed in this version."
                      onChange={handleBulkUpload}
                    ></textarea>
                  </div>
                  <p className="mt-2 text-sm text-gray-500">
                    Note: In this version, only the first URL will be processed.
                  </p>
                </div>

                <div className="flex items-center">
                  <input
                    id="terms"
                    name="terms"
                    type="checkbox"
                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                    required
                  />
                  <label htmlFor="terms" className="ml-2 block text-sm text-gray-900">
                    I understand that this will automate the application process using my selected résumé
                  </label>
                </div>

                <div>
                  <button
                    type="submit"
                    disabled={isSubmitting}
                    className={`inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 ${
                      isSubmitting ? "opacity-50 cursor-not-allowed" : ""
                    }`}
                  >
                    {isSubmitting ? "Submitting..." : "Add Job URL"}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
