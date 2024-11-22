'use client'

export default function MembersPage() {
    return (
        <div className="min-h-screen pt-20 pb-12 px-4">
            <div className="container mx-auto max-w-6xl">
                {/* Header Spot */}
                <div className="flex justify-center">
                    <div className="mb-8">
                        <h1 className="text-3xl md:text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-600 via-pink-500 to-orange-400 font-montserrat">
                            Black Knights Members
                        </h1>
                        <p className="text-gray-600 mt-2">
                            Learn more about the creators of Adversarial Playground!
                        </p>
                    </div>
                </div>
                {/* Jacob, Eli, Ed */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {/* Jacob */}
                    <div className="p-4 bg-white border border-gray-200 rounded-lg shadow-md text-center">
                        <img
                            src="/assets/jacob.jpg"
                            alt="Jacob Huckelberry"
                            className="w-24 h-24 mx-auto rounded-full shadow-lg"
                        />
                        <h2 className="text-xl font-bold text-purple-600 mt-4">Jacob Huckelberry</h2>
                        <p className="text-gray-600 mt-2">Role: Developer</p>
                        <p className="text-gray-500 mt-2">Description about Jacob.</p>
                    </div>

                    {/* Eli */}
                    <div className="p-4 bg-white border border-gray-200 rounded-lg shadow-md text-center">
                        <img
                            src="/assets/eli.jpg"
                            alt="Elijah Dabkowski"
                            className="w-24 h-24 mx-auto rounded-full shadow-lg"
                        />
                        <h2 className="text-xl font-bold text-purple-600 mt-4">Elijah Dabkowski</h2>
                        <p className="text-gray-600 mt-2">Role: Developer</p>
                        <p className="text-gray-500 mt-2">Description about Eli.</p>
                    </div>

                    {/* Ed */}
                    <div className="p-4 bg-white border border-gray-200 rounded-lg shadow-md text-center">
                        <img
                            src="/assets/ed.jpeg"
                            alt="Ed Tang"
                            className="w-24 h-24 mx-auto rounded-full shadow-lg"
                        />
                        <h2 className="text-xl font-bold text-purple-600 mt-4">Ed Tang</h2>
                        <p className="text-gray-600 mt-2">Role: Developer</p>
                        <p className="text-gray-500 mt-2">Description about Ed.</p>
                    </div>
                </div>
            </div>
        </div>
    );
}
