'use client'

export default function AttacksPage() {
    return (
        <div className="min-h-screen pt-20 pb-12 px-4">
            <div className="container mx-auto max-w-6xl">
                {/* Header Spot */}
                <div className="mb-8">
                    <h1 className="text-3xl md:text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-600 via-pink-500 to-orange-400 font-montserrat">
                        Types of Adversarial Attacks
                    </h1>
                </div>

                {/* Types of Attacks */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                    {/* FGSM */}
                    <div className="p-4 bg-white border border-gray-200 rounded-lg shadow-md text-center">
                        <h2 className="text-xl font-bold text-purple-600 mt-4">Fast Gradient Sign Method</h2>
                        <p className="text-gray-600 mt-2">
                            The Fast Gradient Sign Method (FGSM) is an adversarial attack which slightly
                            changes the input data through adding noise based on the gradient of the loss
                            with respect to the input image. While the input will look similar if not identical
                            to the human eye, the attack effects the model it is implemented on by forcing
                            it to misclassify the data. Visit <a href="https://medium.com/@zachariaharungeorge/a-deep-dive-into-the-fast-gradient-sign-method-611826e34865" style={{ color: 'blue', textDecoration: 'underline' }} target="_blank">
                            A Deep Dive into the Fast Gradient Design Method </a>
                             to learn more.
                            </p>
                    </div>

                    {/* PGD */}
                    <div className="p-4 bg-white border border-gray-200 rounded-lg shadow-md text-center">
                        <h2 className="text-xl font-bold text-purple-600 mt-4">Projected Gradient Descent</h2>
                        <p className="text-gray-600 mt-2">
                            The Projected Gradient Descent (PGD) attack is similar to that of the Fast Gradient Sign 
                            method in that an input image is changed based on the model's gradient. It is another white-box 
                            method that requires needs full knowledge of a how a model functions. Read more about the 
                            PGD method here: <a href="https://medium.com/@zachariaharungeorge/a-deep-dive-into-the-fast-gradient-sign-method-611826e34865" style={{ color: 'blue', textDecoration: 'underline' }} target="_blank">
                            Unveiling the Power of Projected Gradient Descent in Adversarial Attacks.</a>
                        </p>
                    </div>

                    {/* DeepFool */}
                    <div className="p-4 bg-white border border-gray-200 rounded-lg shadow-md text-center">
                        <h2 className="text-xl font-bold text-purple-600 mt-4">DeepFool</h2>
                        <p className="text-gray-600 mt-2">
                            The DeepFool attack is an adversarial attack which aims to "create the most minimal perturbations
                            to an image to deceive (a) model". It aims to find a point accross a decision boundary that is 
                            the closest to the original input to cause a model to misclassify the input with the least 
                            amount of modification possible. You can read the paper <a href="https://ieeexplore.ieee.org/document/10134485" style={{ color: 'blue', textDecoration: 'underline' }} target="_blank">
                            Understanding DeepFool Adversarial Attack and Defense with Skater Interpretations </a> to learn more
                        </p>
                    </div>

                    {/* Square */}
                    <div className="p-4 bg-white border border-gray-200 rounded-lg shadow-md text-center">
                        <h2 className="text-xl font-bold text-purple-600 mt-4">Square Attack</h2>
                        <p className="text-gray-600 mt-2">
                            The Square Attack is a black-box attack that enables a user to not need to know the entirety 
                            of how a model works. The attack changes an image by adding square-shaped contiguous
                            pixels, hence the name Square Attack, to an image where once again the change is imperceptible 
                            to the human eye, but to a model the change is enough to misclassify the input. 
                            You can read more about the Square Attack here: <a href="https://arxiv.org/pdf/2201.05001#:~:text=In%20white%2Dbox%20attack%2C%20adversary,interact%20through%20input%20and%20output." style={{ color: 'blue', textDecoration: 'underline' }} target="_blank">
                            Evaluation of Four Black-box Adversarial Attacks and Some Query-efficient Improvement Analysis.</a>
                        </p>
                    </div>

                </div>
            </div>
        </div>
    );
}