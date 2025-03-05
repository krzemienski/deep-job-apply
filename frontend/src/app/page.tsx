import Link from "next/link";

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen">
      {/* Header */}
      <header className="bg-blue-600 text-white p-4 shadow-md">
        <div className="container mx-auto flex justify-between items-center">
          <h1 className="text-2xl font-bold">Deep Job Apply</h1>
          <div className="space-x-4">
            <Link
              href="/login"
              className="px-4 py-2 rounded-md bg-white text-blue-600 hover:bg-blue-100 transition-colors"
            >
              Login
            </Link>
            <Link
              href="/register"
              className="px-4 py-2 rounded-md border border-white hover:bg-blue-500 transition-colors"
            >
              Register
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <main className="flex-grow">
        <section className="bg-gradient-to-b from-blue-500 to-blue-600 text-white py-20">
          <div className="container mx-auto px-4 text-center">
            <h2 className="text-4xl md:text-5xl font-bold mb-6">Automate Your Job Applications</h2>
            <p className="text-xl md:text-2xl mb-8 max-w-3xl mx-auto">
              Upload your résumé once, apply to multiple jobs with a single click using AI-powered automation.
            </p>
            <Link
              href="/register"
              className="px-8 py-3 bg-white text-blue-600 rounded-full text-lg font-semibold hover:bg-blue-50 transition-colors shadow-lg"
            >
              Get Started
            </Link>
          </div>
        </section>

        {/* Features Section */}
        <section className="py-16 bg-white">
          <div className="container mx-auto px-4">
            <h2 className="text-3xl font-bold text-center mb-12">How It Works</h2>
            <div className="grid md:grid-cols-3 gap-8">
              <div className="bg-blue-50 p-6 rounded-lg shadow-sm">
                <div className="text-blue-600 text-4xl font-bold mb-4">1</div>
                <h3 className="text-xl font-semibold mb-2">Upload Your Résumé</h3>
                <p className="text-gray-600">
                  Upload your résumé in PDF format. Our system will automatically parse and extract your information.
                </p>
              </div>
              <div className="bg-blue-50 p-6 rounded-lg shadow-sm">
                <div className="text-blue-600 text-4xl font-bold mb-4">2</div>
                <h3 className="text-xl font-semibold mb-2">Add Job URLs</h3>
                <p className="text-gray-600">
                  Paste URLs of job listings you&apos;re interested in from any major job board.
                </p>
              </div>
              <div className="bg-blue-50 p-6 rounded-lg shadow-sm">
                <div className="text-blue-600 text-4xl font-bold mb-4">3</div>
                <h3 className="text-xl font-semibold mb-2">Let AI Do the Work</h3>
                <p className="text-gray-600">
                  Our system automatically navigates to each job listing, fills out applications, and submits them on your behalf.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Benefits Section */}
        <section className="py-16 bg-gray-50">
          <div className="container mx-auto px-4">
            <h2 className="text-3xl font-bold text-center mb-12">Why Use Deep Job Apply?</h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="p-4">
                <h3 className="text-xl font-semibold mb-2">Save Time</h3>
                <p className="text-gray-600">
                  Apply to dozens of jobs in minutes instead of hours.
                </p>
              </div>
              <div className="p-4">
                <h3 className="text-xl font-semibold mb-2">Increase Applications</h3>
                <p className="text-gray-600">
                  Apply to more positions and increase your chances of getting interviews.
                </p>
              </div>
              <div className="p-4">
                <h3 className="text-xl font-semibold mb-2">Reduce Stress</h3>
                <p className="text-gray-600">
                  Eliminate the tedium of filling out the same information repeatedly.
                </p>
              </div>
              <div className="p-4">
                <h3 className="text-xl font-semibold mb-2">Track Progress</h3>
                <p className="text-gray-600">
                  Monitor all your applications in one dashboard.
                </p>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-8">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="mb-4 md:mb-0">
              <h2 className="text-xl font-bold">Deep Job Apply</h2>
              <p className="text-gray-400">Automated job application system</p>
            </div>
            <div className="flex space-x-4">
              <Link href="/about" className="hover:text-blue-300">About</Link>
              <Link href="/privacy" className="hover:text-blue-300">Privacy</Link>
              <Link href="/terms" className="hover:text-blue-300">Terms</Link>
              <Link href="/contact" className="hover:text-blue-300">Contact</Link>
            </div>
          </div>
          <div className="mt-8 text-center text-gray-400 text-sm">
            &copy; {new Date().getFullYear()} Deep Job Apply. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
}
