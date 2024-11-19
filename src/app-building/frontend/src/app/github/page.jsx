'use client'

export default function GitHubPage() {
    return (
        <div className="min-h-screen pt-20 pb-12 px-4">
            <div className="container mx-auto max-w-6xl">
                {/* Header */}
                <div className="mb-8">
                    <h1 className="text-3xl md:text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-600 via-pink-500 to-orange-400 font-montserrat">
                        GitHub Page
                    </h1>
                    <p className="text-gray-600 mt-2">
                        Observe our source code!
                    </p>
                </div>

                {/* Button */}
                <div>
                    <a 
                        href="https://github.com/huckels15/AC215_BlackKnights/tree/app_dev" // Replace with your GitHub URL
                        target="_blank"
                        rel="noopener noreferrer"
                        className="px-4 py-2 bg-purple-600 text-white font-bold rounded-lg shadow-lg hover:bg-purple-700 transition-colors"
                    >
                        Visit GitHub
                    </a>
                </div>
            </div>
        </div>
    );
}
