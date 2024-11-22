'use client'

import { useState } from 'react';
import { getFGSMRes } from '@/components/playground/FGSMRes';
import { getPGDRes } from '@/components/playground/PGDRes';
import { getDEEPFOOLRes } from '@/components/playground/DEEPFOOLRes';
import { getSQUARERes } from '@/components/playground/SQUARERes';
import { getFGSMAlex } from '@/components/playground/FGSMAlex';
import { getPGDAlex } from '@/components/playground/PGDAlex';
import { getDEEPFOOLAlex } from '@/components/playground/DEEPFOOLAlex';
import { getSQUAREAlex } from '@/components/playground/SQUAREAlex';

export default function PlaygroundPage() {
    const [selectedModel, setSelectedModel] = useState('');
    const [selectedAttack, setSelectedAttack] = useState('');
    const [output, setOutput] = useState('');
    const [plotOutput, setPlot] = useState('');
    const [loading, setLoading] = useState(false);

    const handleModelChange = (event) => {
        setSelectedModel(event.target.value);
    };

    const handleAttackChange = (event) => {
        setSelectedAttack(event.target.value);
    };

    const handleRun = async () => {
        if (selectedModel && selectedAttack) {
            if (selectedModel === "resnet" && selectedAttack === "fgsm") {
                setLoading(true);
                try {
                    const result = await getFGSMRes(selectedModel, selectedAttack);

                    if (result.error) {
                        setOutput('Failed to fetch response.');
                        console.error(result.error);
                    } else {
                        setOutput(result.json);
                        setPlot(result.image);
                    }
                } catch (error) {
                    setOutput("Failed to fetch response.");
                } finally {
                    setLoading(false);
                }
            } else if (selectedModel === "resnet" && selectedAttack === "pgd") {
                setLoading(true);
                try {
                    const result = await getPGDRes(selectedModel, selectedAttack);

                    if (result.error) {
                        setOutput('Failed to fetch response.');
                        console.error(result.error);
                    } else {
                        setOutput(result.json);
                        setPlot(result.image);
                    }
                } catch (error) {
                    setOutput("Failed to fetch response.");
                } finally {
                    setLoading(false);
                }
            } else if (selectedModel === "resnet" && selectedAttack === "deepfool") {
                setLoading(true);
                try {
                    const result = await getDEEPFOOLRes(selectedModel, selectedAttack);

                    if (result.error) {
                        setOutput('Failed to fetch response.');
                        console.error(result.error);
                    } else {
                        setOutput(result.json);
                        setPlot(result.image);
                    }
                } catch (error) {
                    setOutput("Failed to fetch response.");
                } finally {
                    setLoading(false);
                }
            } else if (selectedModel === "resnet" && selectedAttack === "square") {
                setLoading(true);
                try {
                    const result = await getSQUARERes(selectedModel, selectedAttack);

                    if (result.error) {
                        setOutput('Failed to fetch response.');
                        console.error(result.error);
                    } else {
                        setOutput(result.json);
                        setPlot(result.image);
                    }
                } catch (error) {
                    setOutput("Failed to fetch response.");
                } finally {
                    setLoading(false);
                }
            } else if (selectedModel === "alexnet" && selectedAttack === "fgsm") {
                setLoading(true);
                try {
                    const result = await getFGSMAlex(selectedModel, selectedAttack);

                    if (result.error) {
                        setOutput('Failed to fetch response.');
                        console.error(result.error);
                    } else {
                        setOutput(result.json);
                        setPlot(result.image);
                    }
                } catch (error) {
                    setOutput("Failed to fetch response.");
                } finally {
                    setLoading(false);
                }
            } else if (selectedModel === "alexnet" && selectedAttack === "pgd") {
                setLoading(true);
                try {
                    const result = await getPGDAlex(selectedModel, selectedAttack);

                    if (result.error) {
                        setOutput('Failed to fetch response.');
                        console.error(result.error);
                    } else {
                        setOutput(result.json);
                        setPlot(result.image);
                    }
                } catch (error) {
                    setOutput("Failed to fetch response.");
                } finally {
                    setLoading(false);
                }
            } else if (selectedModel === "alexnet" && selectedAttack === "deepfool") {
                setLoading(true);
                try {
                    const result = await getDEEPFOOLAlex(selectedModel, selectedAttack);

                    if (result.error) {
                        setOutput('Failed to fetch response.');
                        console.error(result.error);
                    } else {
                        setOutput(result.json);
                        setPlot(result.image);
                    }
                } catch (error) {
                    setOutput("Failed to fetch response.");
                } finally {
                    setLoading(false);
                }
            } else if (selectedModel === "alexnet" && selectedAttack === "square") {
                try {
                    const result = await getSQUAREAlex(selectedModel, selectedAttack);

                    if (result.error) {
                        setOutput('Failed to fetch response.');
                        console.error(result.error);
                    } else {
                        setOutput(result.json);
                        setPlot(result.image);
                    }
                } catch (error) {
                    setOutput("Failed to fetch response.");
                } finally {
                    setLoading(false);
                }
            } else {
                setOutput("Selected model or attack does not match any valid combinations.");
            }
        } else {
            setOutput("Please select both a model and an attack.");
        }
    };

    return (
        <div className="min-h-screen pt-20 pb-12 px-4">
            <div className="container mx-auto max-w-6xl">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    {/* User Selection */}
                    <div>
                        {/* Select Model */}
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
                                    <option value="alexnet">AlexNet</option>
                                </select>
                            </div>
                        </div>

                        {/* Select Attack */}
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
                                    <option value="deepfool">DeepFool</option>
                                    <option value="square">Square Attack</option>
                                </select>
                            </div>
                        </div>
                    </div>

                    {/* Display Backend Output */}
                    <div className="flex flex-col items-center justify-center">
                        {/* Instance to handle backend output */}
                        <button
                            onClick={handleRun}
                            className="mb-8 px-6 py-2 bg-green-600 text-white font-bold rounded-lg shadow-lg hover:bg-green-700 transition-colors"
                        >
                            Let's Play!
                        </button>

                        {/* Load Output */}
                        <div className="text-center">
                            <h2 className="text-xl font-bold text-gray-700">Output</h2>
                            <div className="mt-4">
                                {loading ? (
                                    <p className="text-gray-600">Loading...</p>
                                ) : (
                                    <>
                                      {output.reg_acc && output.adv_acc ? (
                                        <div className="bg-gray-100 p-4 rounded-lg shadow-inner text-left">
                                          <p className="text-gray-700">
                                            <span className="font-bold">Accuracy Before Attack:</span> {output.reg_acc}
                                          </p>
                                          <p className="text-gray-700">
                                            <span className="font-bold">Accuracy After Attack:</span> {output.adv_acc}
                                          </p>
                                        </div>
                                      ) : (
                                        <p className="text-red-600">{output}</p>
                                      )}
                  
                                      {/* Show Before and After Image */}
                                      {plotOutput && (
                                        <img
                                          src={plotOutput}
                                          alt="Resulting Adversarial Example"
                                          className="mt-4 max-w-full rounded-lg shadow-md"
                                        />
                                      )}
                                    </>
                                  )}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
