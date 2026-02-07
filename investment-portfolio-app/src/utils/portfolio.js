export async function fetchPortfolio({ budget, risk, horizon }) {
  const horizonMap = {
    "3m": "3_months",
    "6m": "6_months",
    "1y": "1_year",
    "2y": "2_years",
    "3y": "3_years",
    "5y": "5_years",
  };

  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/api/portfolio/build`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        budget_ngn: Number(budget),
        risk_level: risk,
        time_horizon: horizonMap[horizon] || "1_year",
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error?.message || "Failed to build portfolio");
    }

    return await response.json();
  } catch (err) {
    throw new Error(err.message || "Connection to backend failed.");
  }
}
