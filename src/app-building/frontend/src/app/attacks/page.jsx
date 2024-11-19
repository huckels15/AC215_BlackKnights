'use client'

export default function AttacksPage() {
    return (
        <div className="min-h-screen pt-20 pb-12 px-4">
            <div className="container mx-auto max-w-6xl">
                {/* Header */}
                <div className="mb-8">
                    <h1 className="text-3xl md:text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-600 via-pink-500 to-orange-400 font-montserrat">
                        Adversarial Attacks
                    </h1>
                    <p className="text-gray-600 mt-2">
                        Learn more about the adversarial attacks implemented
                    </p>
                </div>

                {/* Attack Section */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                    {/* Attack 1 */}
                    <div className="p-4 bg-white border border-gray-200 rounded-lg shadow-md text-center">
                        <h2 className="text-xl font-bold text-purple-600 mt-4">Fast Gradient Sign Method</h2>
                        <p className="text-gray-600 mt-2">Fast Gradient Sign Method Description</p>
                    </div>

                    {/* Attack 2 */}
                    <div className="p-4 bg-white border border-gray-200 rounded-lg shadow-md text-center">
                        <h2 className="text-xl font-bold text-purple-600 mt-4">Projected Gradient Descent</h2>
                        <p className="text-gray-600 mt-2">Projected Gradient Descent Description</p>
                    </div>

                    {/* Attack 3 */}
                    <div className="p-4 bg-white border border-gray-200 rounded-lg shadow-md text-center">
                        <h2 className="text-xl font-bold text-purple-600 mt-4">DeepFool</h2>
                        <p className="text-gray-600 mt-2">DeepFool Description</p>
                    </div>

                    {/* Attack 4 */}
                    <div className="p-4 bg-white border border-gray-200 rounded-lg shadow-md text-center">
                        <h2 className="text-xl font-bold text-purple-600 mt-4">Square Attack</h2>
                        <p className="text-gray-600 mt-2">Square Attack Description</p>
                    </div>

                </div>
            </div>
        </div>
    );
}