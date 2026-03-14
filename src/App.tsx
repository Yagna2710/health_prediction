import React, { useState } from 'react';
import { Activity, Heart, Shield, AlertTriangle, CheckCircle, Clock, Utensils, IndianRupee, Loader2 } from 'lucide-react';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid } from 'recharts';

function App() {
  const [formData, setFormData] = useState({
    Age: '',
    Gender: 'Male',
    BMI: '',
    Smoking: 'No',
    BloodPressure: 'Normal',
    Diabetes: '0',
    ChronicCond_Cancer: '0',
    ChronicCond_Heartfailure: '0',
    Respiratory_Issues: 'No',
    Children: '0',
    ClaimHistory_Frequency: '0',
    HospitalizationHistory: 'No'
  });

  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<any>(null);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await fetch('http://localhost:5000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      const data = await response.json();
      if (data.success) {
        setResults(data);
      } else {
        alert('Error predicting risk: ' + data.error);
      }
    } catch (error) {
      alert('Failed to connect to backend server. Make sure it is running.');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const COLORS = ['#10b981', '#f59e0b', '#ef4444'];
  const getRiskColor = (level: string) => {
    if (level === 'Low Risk') return 'text-green-500';
    if (level === 'Medium Risk') return 'text-yellow-500';
    return 'text-red-500';
  };
  
  const getRiskBgColor = (level: string) => {
    if (level === 'Low Risk') return 'bg-green-100 border-green-500';
    if (level === 'Medium Risk') return 'bg-yellow-100 border-yellow-500';
    return 'bg-red-100 border-red-500';
  };

  const chartData = results ? [
    { name: 'Healthy', value: Math.max(0, 100 - (results.prediction.risk_probability * 100)) },
    { name: 'Risk', value: results.prediction.risk_probability * 100 }
  ] : [];

  const costData = results ? [
    { name: 'Avg Claim', cost: results.analytics.average_claim },
    { name: 'Est Cost', cost: results.analytics.estimated_cost },
    { name: 'Coverage', cost: results.insurance.coverage_amount / 10 } // scaled for chart
  ] : [];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-slate-50 to-indigo-50/30 text-slate-800 p-4 md:p-8 font-sans transition-colors duration-500">
      <header className="max-w-7xl mx-auto flex items-center justify-between mb-8 pb-4 pt-2 border-b border-slate-200/60">
        <div className="flex items-center gap-3 text-blue-600">
          <Activity size={32} />
          <h1 className="text-2xl md:text-3xl font-bold">Predictive Risk & Care Management</h1>
        </div>
        <div className="text-sm font-medium text-slate-500">
          PGDM Project Dashboard
        </div>
      </header>

      <main className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        
        {/* Left Column: Form */}
        <section className="lg:col-span-4 bg-white/80 backdrop-blur-sm rounded-2xl shadow-sm border border-slate-200/60 p-6 overflow-hidden hover:shadow-md transition-shadow duration-300">
          <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
            <Heart className="text-rose-500" size={24} /> 
            User Health Profile
          </h2>
          
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Age</label>
                <input type="number" required name="Age" value={formData.Age} onChange={handleInputChange} className="w-full rounded-lg border-slate-200 border p-2.5 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 focus:outline-none transition-all duration-200 bg-slate-50/50 hover:bg-white" />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Gender</label>
                <select name="Gender" value={formData.Gender} onChange={handleInputChange} className="w-full rounded-lg border-slate-200 border p-2.5 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 focus:outline-none transition-all duration-200 bg-slate-50/50 hover:bg-white">
                  <option>Male</option>
                  <option>Female</option>
                </select>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">BMI</label>
                <input type="number" step="0.1" required name="BMI" value={formData.BMI} onChange={handleInputChange} className="w-full rounded-lg border-slate-200 border p-2.5 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 focus:outline-none transition-all duration-200 bg-slate-50/50 hover:bg-white" />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Smoking</label>
                <select name="Smoking" value={formData.Smoking} onChange={handleInputChange} className="w-full rounded-lg border-slate-200 border p-2.5 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 focus:outline-none transition-all duration-200 bg-slate-50/50 hover:bg-white">
                  <option>No</option>
                  <option>Yes</option>
                </select>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Blood Pressure</label>
                <select name="BloodPressure" value={formData.BloodPressure} onChange={handleInputChange} className="w-full rounded-lg border-slate-200 border p-2.5 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 focus:outline-none transition-all duration-200 bg-slate-50/50 hover:bg-white">
                  <option>Normal</option>
                  <option>High</option>
                  <option>Low</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Diabetes Status</label>
                <select name="Diabetes" value={formData.Diabetes} onChange={handleInputChange} className="w-full rounded-lg border-slate-200 border p-2.5 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 focus:outline-none transition-all duration-200 bg-slate-50/50 hover:bg-white">
                  <option value="0">No</option>
                  <option value="1">Yes</option>
                </select>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Heart Disease</label>
                <select name="ChronicCond_Heartfailure" value={formData.ChronicCond_Heartfailure} onChange={handleInputChange} className="w-full rounded-lg border-slate-200 border p-2.5 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 focus:outline-none transition-all duration-200 bg-slate-50/50 hover:bg-white">
                  <option value="0">No</option>
                  <option value="1">Yes</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Cancer</label>
                <select name="ChronicCond_Cancer" value={formData.ChronicCond_Cancer} onChange={handleInputChange} className="w-full rounded-lg border-slate-200 border p-2.5 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 focus:outline-none transition-all duration-200 bg-slate-50/50 hover:bg-white">
                  <option value="0">No</option>
                  <option value="1">Yes</option>
                </select>
              </div>
            </div>
            
            <div className="grid grid-cols-2 gap-4">
               <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Respiratory Issues</label>
                  <select name="Respiratory_Issues" value={formData.Respiratory_Issues} onChange={handleInputChange} className="w-full rounded-lg border-slate-200 border p-2.5 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 focus:outline-none transition-all duration-200 bg-slate-50/50 hover:bg-white">
                     <option>No</option>
                     <option>Yes</option>
                  </select>
               </div>
               <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Number of Children</label>
                  <input type="number" required min="0" name="Children" value={formData.Children} onChange={handleInputChange} className="w-full rounded-lg border-slate-200 border p-2.5 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 focus:outline-none transition-all duration-200 bg-slate-50/50 hover:bg-white" />
               </div>
            </div>
            
            <div className="grid grid-cols-2 gap-4">
               <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Claim History (Yearly)</label>
                  <select name="ClaimHistory_Frequency" value={formData.ClaimHistory_Frequency} onChange={handleInputChange} className="w-full rounded-lg border-slate-200 border p-2.5 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 focus:outline-none transition-all duration-200 bg-slate-50/50 hover:bg-white">
                     <option value="0">0</option>
                     <option value="1-2">1-2</option>
                     <option value="3+">3+</option>
                  </select>
               </div>
               <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Past Hospitalization</label>
                  <select name="HospitalizationHistory" value={formData.HospitalizationHistory} onChange={handleInputChange} className="w-full rounded-lg border-slate-200 border p-2.5 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 focus:outline-none transition-all duration-200 bg-slate-50/50 hover:bg-white">
                     <option>No</option>
                     <option>Yes</option>
                  </select>
               </div>
            </div>

            <button type="submit" disabled={loading} className="w-full mt-6 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-bold py-3 px-4 rounded-xl shadow-md hover:shadow-lg transform transition-all duration-200 hover:-translate-y-0.5 disabled:opacity-70 disabled:cursor-not-allowed flex items-center justify-center gap-2">
              {loading ? <><Loader2 className="animate-spin" size={20} /> Analyzing Data...</> : 'Generate Prediction'}
            </button>
          </form>
        </section>

        {/* Right Column: Results Dashboard */}
        <section className="lg:col-span-8 flex flex-col gap-6">
          
          {results ? (
            <>
              {/* Top Row: Risk Prediction and Claim Analytics */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                
                {/* Risk Prediction Card */}
                <div className={`rounded-2xl border-l-4 p-6 shadow-sm hover:shadow-md transition-all duration-300 hover:-translate-y-1 bg-white/90 backdrop-blur-sm ${getRiskBgColor(results.prediction.risk_level)}`}>
                  <div className="flex justify-between items-start mb-4">
                    <h3 className="text-lg font-bold flex items-center gap-2">
                       <AlertTriangle className={getRiskColor(results.prediction.risk_level)} />
                       Risk Prediction
                    </h3>
                    <span className={`px-3 py-1 rounded-full text-sm font-bold bg-white shadow-sm ${getRiskColor(results.prediction.risk_level)}`}>
                      {results.prediction.risk_level}
                    </span>
                  </div>
                  
                  <div className="flex items-center justify-between mt-6">
                    <div className="w-32 h-32">
                       <ResponsiveContainer width="100%" height="100%">
                         <PieChart>
                           <Pie data={chartData} innerRadius={35} outerRadius={50} dataKey="value" stroke="none">
                             {chartData.map((entry, index) => (
                               <Cell key={`cell-${index}`} fill={index === 0 ? '#10b981' : (results.prediction.risk_level === 'High Risk' ? '#ef4444' : '#f59e0b')} />
                             ))}
                           </Pie>
                         </PieChart>
                       </ResponsiveContainer>
                    </div>
                    <div className="text-right">
                      <p className="text-sm text-slate-500 uppercase tracking-wide">Risk Probability</p>
                      <p className={`text-4xl font-extrabold ${getRiskColor(results.prediction.risk_level)}`}>
                        {(results.prediction.risk_probability * 100).toFixed(0)}%
                      </p>
                      <p className="text-sm mt-2 text-slate-600 font-medium">
                        Key Factors: {results.prediction.key_factors.join(', ')}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Claim Analytics Card */}
                <div className="bg-white/90 backdrop-blur-sm rounded-2xl shadow-sm hover:shadow-md transition-all duration-300 hover:-translate-y-1 border border-slate-200/60 p-6">
                  <h3 className="text-lg font-bold mb-4 flex items-center gap-2 text-slate-800">
                    <Activity className="text-purple-500" /> Claim Risk Analytics
                  </h3>
                  <div className="space-y-4 text-sm">
                     <div className="flex justify-between items-center bg-slate-50 p-2 rounded-lg border border-slate-100">
                        <span className="text-slate-600">Claim Frequency</span>
                        <span className="font-bold text-slate-800">{results.analytics.claim_frequency}</span>
                     </div>
                     <div className="flex justify-between items-center bg-slate-50 p-2 rounded-lg border border-slate-100">
                        <span className="text-slate-600">Future Probability</span>
                        <span className="font-bold text-slate-800">{(results.analytics.future_claim_probability * 100).toFixed(1)}%</span>
                     </div>
                     <div className="flex justify-between items-center bg-slate-50 p-2 rounded-lg border border-slate-100">
                        <span className="text-slate-600">Abnormal Patterns</span>
                        <span className="font-bold text-rose-600">{results.analytics.fraud_or_abnormal_patterns}</span>
                     </div>
                     <div className="flex justify-between items-center bg-purple-50 p-3 rounded-lg border border-purple-100">
                        <span className="text-purple-700 font-medium">Est. Future Cost</span>
                        <span className="font-bold text-purple-700 flex items-center text-lg">
                           <IndianRupee size={18} />{results.analytics.estimated_cost.toLocaleString('en-IN')}/yr
                        </span>
                     </div>
                  </div>
                </div>

              </div>

              {/* Bottom Row: Insurance & Preventive Care */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                
                {/* Insurance Recommendation */}
                <div className="bg-gradient-to-br from-blue-50/80 to-white/90 backdrop-blur-sm rounded-2xl shadow-sm hover:shadow-md transition-all duration-300 hover:-translate-y-1 border border-blue-200/60 p-6">
                  <h3 className="text-lg font-bold mb-4 flex items-center gap-2 text-blue-800">
                    <Shield className="text-blue-600" /> Insurance Recommendation
                  </h3>
                  
                  <div className="mb-4 pb-4 border-b border-blue-100">
                     <p className="text-sm text-blue-600 uppercase tracking-wide font-semibold mb-1">Recommended Plan</p>
                     <p className="text-2xl font-bold text-slate-800">{results.insurance.recommended_plan}</p>
                  </div>
                  
                  <div className="grid grid-cols-2 gap-4">
                     <div>
                        <p className="text-sm text-slate-500">Coverage Suggestion</p>
                        <p className="text-lg font-bold text-slate-800">
                           {results.insurance.coverage_suggestion}
                        </p>
                     </div>
                     <div>
                        <p className="text-sm text-slate-500">Premium Range</p>
                        <p className="text-lg font-bold text-blue-600">
                           {results.insurance.premium_range}
                        </p>
                     </div>
                  </div>
                  <div className="mt-4 text-sm text-slate-600 bg-blue-50/50 p-3 rounded-lg border border-blue-100">
                     <p className="font-semibold text-blue-800 mb-1">Reason for Recommendation:</p>
                     <p>{results.insurance.reason}</p>
                  </div>
                </div>

                {/* Preventive Care */}
                <div className="bg-gradient-to-br from-emerald-50/80 to-white/90 backdrop-blur-sm rounded-2xl shadow-sm hover:shadow-md transition-all duration-300 hover:-translate-y-1 border border-emerald-200/60 p-6">
                  <h3 className="text-lg font-bold mb-4 flex items-center gap-2 text-emerald-800">
                    <CheckCircle className="text-emerald-600" /> Preventive Care Management
                  </h3>
                  
                  <div className="space-y-4">
                     <div>
                        <h4 className="text-sm font-bold text-slate-700 flex items-center gap-1 mb-1">
                           <Shield size={16} className="text-emerald-500" /> Required Actions
                        </h4>
                        <ul className="list-disc list-inside text-sm text-slate-600 ml-1 space-y-1">
                           {results.preventive_care.preventive_actions.map((it: string, i: number) => <li key={i}>{it}</li>)}
                        </ul>
                     </div>
                     
                     <div>
                        <h4 className="text-sm font-bold text-slate-700 flex items-center gap-1 mb-1">
                           <Activity size={16} className="text-blue-500" /> Recommended Checkups
                        </h4>
                        <ul className="list-disc list-inside text-sm text-slate-600 ml-1 space-y-1">
                           {results.preventive_care.health_recommendations_checkups.map((it: string, i: number) => <li key={i}>{it}</li>)}
                        </ul>
                     </div>

                     <div>
                        <h4 className="text-sm font-bold text-slate-700 flex items-center gap-1 mb-1">
                           <Utensils size={16} className="text-orange-500" /> Lifestyle Tips
                        </h4>
                        <ul className="list-disc list-inside text-sm text-slate-600 ml-1 space-y-1">
                           {results.preventive_care.lifestyle_improvement_tips.map((it: string, i: number) => <li key={i}>{it}</li>)}
                        </ul>
                     </div>
                  </div>
                </div>

              </div>
            </>
          ) : (
            <div className="h-full flex items-center justify-center bg-white/60 backdrop-blur-sm rounded-2xl border border-slate-200/60 shadow-sm p-12 text-center text-slate-500">
               <div>
                  <Activity size={48} className="mx-auto text-blue-200 mb-4" />
                  <h3 className="text-xl font-medium text-slate-700 mb-2">No Data Analyzed Yet</h3>
                  <p className="max-w-md mx-auto">Fill out the patient health profile on the left and click "Generate Prediction" to see the comprehensive risk analysis, insurance recommendations, and preventive care plan.</p>
               </div>
            </div>
          )}

        </section>

      </main>
    </div>
  );
}

export default App;
