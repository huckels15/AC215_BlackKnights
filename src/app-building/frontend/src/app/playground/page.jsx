'use client'

import { useState } from 'react';
import { getMockResponse } from '@/components/playground/Playground';

export default function PlaygroundPage() {
    const [selectedModel, setSelectedModel] = useState('');
    const [selectedAttack, setSelectedAttack] = useState('');
    const [output, setOutput] = useState(''); // To display the API response
    const [loading, setLoading] = useState(false); // To show loading state

    const handleModelChange = (event) => {
        setSelectedModel(event.target.value);
    };

    const handleAttackChange = (event) => {
        setSelectedAttack(event.target.value);
    };

    const handleRun = async () => {
        if (selectedModel && selectedAttack) {
            setLoading(true); // Show loading spinner
            try {
                const response = await getMockResponse(selectedModel, selectedAttack);
                setOutput(JSON.stringify(response, null, 2)); // Display JSON response
            } catch (error) {
                setOutput("Failed to fetch response.");
            } finally {
                setLoading(false); // Stop loading spinner
            }
        } else {
            setOutput("Please select both a model and an attack.");
        }
    };

    return (
        <div className="min-h-screen pt-20 pb-12 px-4">
            <div className="container mx-auto max-w-6xl">
                {/* Two Column Layout */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    {/* Left Column: Selections */}
                    <div>
                        {/* Model Selection */}
                        <div className="mb-8">
                            <h1 className="text-2xl md:text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-600 via-pink-500 to-orange-400 font-montserrat">
                                Select a Model
                            </h1>
                            <div className="mt-4">
                                <select
                                    value={selectedModel}
                                    onChange={handleModelChange}
                                    className="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-md focus:outline-none focus:ring-2 focus:ring-purple-600"
                                >
                                    <option value="" disabled>
                                        Choose a Model
                                    </option>
                                    <option value="resnet">ResNet</option>
                                    <option value="yolo">Yolo</option>
                                </select>
                            </div>
                        </div>

                        {/* Attack Selection */}
                        <div className="mb-8">
                            <h1 className="text-2xl md:text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-600 via-pink-500 to-orange-400 font-montserrat">
                                Select an Attack
                            </h1>
                            <div className="mt-4">
                                <select
                                    value={selectedAttack}
                                    onChange={handleAttackChange}
                                    className="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-md focus:outline-none focus:ring-2 focus:ring-purple-600"
                                >
                                    <option value="" disabled>
                                        Choose an Attack
                                    </option>
                                    <option value="fgsm">Fast Gradient Sign Method</option>
                                    <option value="pgd">Projected Gradient Descent</option>
                                    <option value="df">DeepFool</option>
                                    <option value="sa">Square Attack</option>
                                </select>
                            </div>
                        </div>
                    </div>

                    {/* Right Column: Run Button and Output */}
                    <div className="flex flex-col items-center justify-center">
                        {/* Run Button */}
                        <button
                            onClick={handleRun}
                            className="mb-8 px-6 py-2 bg-green-600 text-white font-bold rounded-lg shadow-lg hover:bg-green-700 transition-colors"
                        >
                            Let's Play!
                        </button>

                        {/* Output Section */}
                        <div className="text-center">
                            <h2 className="text-xl font-bold text-gray-700">Output</h2>
                            <div className="mt-4">
                                {loading ? (
                                    <p className="text-gray-600">Loading...</p>
                                ) : (
                                    <pre className="text-gray-600 text-left bg-gray-100 p-4 rounded-lg shadow-inner overflow-x-auto">
                                        {output}
                                    </pre>
                                )}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
