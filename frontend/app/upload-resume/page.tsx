"use client";

import { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { useRouter } from "next/navigation";
import axios from "axios";

export default function UploadResumePage() {
    const [file, setFile] = useState<File | null>(null);
    const [uploading, setUploading] = useState(false);
    const [parsing, setParsing] = useState(false);
    const [parsedData, setParsedData] = useState<any>(null);
    const [error, setError] = useState("");
    const router = useRouter();

    const onDrop = useCallback((acceptedFiles: File[]) => {
        if (acceptedFiles?.length > 0) {
            setFile(acceptedFiles[0]);
            setError("");
        }
    }, []);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            "application/pdf": [".pdf"],
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [".docx"],
            "application/msword": [".doc"],
        },
        maxFiles: 1,
    });

    const handleUploadAndParse = async () => {
        if (!file) return;

        setUploading(true);
        setError("");

        try {
            const token = localStorage.getItem("token");
            if (!token) {
                router.push("/login");
                return;
            }

            const formData = new FormData();
            formData.append("file", file);

            // 1. Upload
            const uploadRes = await axios.post("http://localhost:8000/resume/upload", formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                    Authorization: `Bearer ${token}`,
                },
            });

            const { file_path } = uploadRes.data;

            // 2. Parse
            setUploading(false);
            setParsing(true);

            const parseRes = await axios.post(
                `http://localhost:8000/resume/parse?file_path=${encodeURIComponent(file_path)}`,
                {},
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );

            setParsedData({ ...parseRes.data, file_path }); // Keep file_path for saving
            setParsing(false);
        } catch (err: any) {
            console.error(err);
            setError(err.response?.data?.detail || "An error occurred during upload/parsing");
            setUploading(false);
            setParsing(false);
        }
    };

    const handleSaveProfile = async () => {
        if (!parsedData) return;

        try {
            const token = localStorage.getItem("token");
            await axios.post("http://localhost:8000/resume/save", parsedData, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            alert("Profile saved successfully!");
            alert("Profile saved successfully!");
            router.push("/recommended-jobs");
        } catch (err: any) {
            console.error(err);
            setError(err.response?.data?.detail || "Failed to save profile");
        }
    };

    const handleFieldChange = (field: string, value: any) => {
        setParsedData((prev: any) => ({ ...prev, [field]: value }));
    };

    if (parsedData) {
        return (
            <div className="min-h-screen bg-gray-100 p-8">
                <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-md p-6">
                    <h1 className="text-3xl font-bold text-gray-900 mb-6">Review & Edit Profile</h1>

                    <div className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Full Name</label>
                            <input
                                type="text"
                                value={parsedData.name || ""}
                                onChange={(e) => handleFieldChange("name", e.target.value)}
                                className="w-full px-3 py-2 mt-1 border rounded-md"
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Email</label>
                            <input
                                type="email"
                                value={parsedData.email || ""}
                                onChange={(e) => handleFieldChange("email", e.target.value)}
                                className="w-full px-3 py-2 mt-1 border rounded-md"
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Phone</label>
                            <input
                                type="text"
                                value={parsedData.phone || ""}
                                onChange={(e) => handleFieldChange("phone", e.target.value)}
                                className="w-full px-3 py-2 mt-1 border rounded-md"
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Location</label>
                            <input
                                type="text"
                                value={parsedData.location || ""}
                                onChange={(e) => handleFieldChange("location", e.target.value)}
                                placeholder="e.g. Mumbai, India"
                                className="w-full px-3 py-2 mt-1 border rounded-md"
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700">Skills (comma separated)</label>
                            <input
                                type="text"
                                value={parsedData.skills.join(", ")}
                                onChange={(e) => handleFieldChange("skills", e.target.value.split(",").map((s: string) => s.trim()))}
                                className="w-full px-3 py-2 mt-1 border rounded-md"
                            />
                        </div>

                        <div>
                            <h3 className="text-lg font-medium text-gray-900 mt-4">Experience (one per line)</h3>
                            <textarea
                                value={parsedData.experience.join("\n")}
                                onChange={(e) => handleFieldChange("experience", e.target.value.split("\n"))}
                                className="w-full px-3 py-2 mt-1 border rounded-md h-32"
                            />
                        </div>

                        <div>
                            <h3 className="text-lg font-medium text-gray-900 mt-4">Education (one per line)</h3>
                            <textarea
                                value={parsedData.education.join("\n")}
                                onChange={(e) => handleFieldChange("education", e.target.value.split("\n"))}
                                className="w-full px-3 py-2 mt-1 border rounded-md h-24"
                            />
                        </div>

                        <div className="flex justify-end space-x-4 mt-6">
                            <button
                                onClick={() => setParsedData(null)}
                                className="px-4 py-2 text-gray-700 bg-gray-200 rounded-md hover:bg-gray-300"
                            >
                                Cancel
                            </button>
                            <button
                                onClick={handleSaveProfile}
                                className="px-4 py-2 text-white bg-primary-600 rounded-md hover:bg-primary-700"
                            >
                                Confirm & Save Profile
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="flex min-h-screen items-center justify-center bg-gray-100 p-4">
            <div className="w-full max-w-xl p-8 bg-white rounded-lg shadow-md">
                <h1 className="text-2xl font-bold text-center text-gray-900 mb-6">Upload Resume</h1>

                {error && <div className="p-3 mb-4 text-red-500 bg-red-100 rounded">{error}</div>}

                <div
                    {...getRootProps()}
                    className={`border-2 border-dashed rounded-lg p-10 text-center cursor-pointer transition-colors ${isDragActive ? "border-primary-500 bg-primary-50" : "border-gray-300 hover:border-primary-400"
                        }`}
                >
                    <input {...getInputProps()} />
                    {file ? (
                        <p className="text-gray-700 font-medium">{file.name}</p>
                    ) : (
                        <p className="text-gray-500">Drag & drop a resume (PDF/DOCX) here, or click to select</p>
                    )}
                </div>

                <button
                    onClick={handleUploadAndParse}
                    disabled={!file || uploading || parsing}
                    className={`w-full mt-6 px-4 py-2 text-white rounded-md focus:outline-none ${!file || uploading || parsing
                        ? "bg-gray-400 cursor-not-allowed"
                        : "bg-primary-600 hover:bg-primary-700"
                        }`}
                >
                    {uploading ? "Uploading..." : parsing ? "Parsing..." : "Upload & Parse"}
                </button>
            </div>
        </div>
    );
}
