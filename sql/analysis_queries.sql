-- Top Industries by Layoffs
-- Business Question: Which industries were most affected by layoffs?
SELECT industry, SUM(total_laid_off) AS total
FROM layoffs
GROUP BY industry
ORDER BY total DESC
LIMIT 10;

-- Top Countries by Layoffs
-- Business Question: Which countries experienced the highest number of layoffs?
SELECT country, SUM(total_laid_off) AS total
FROM layoffs
GROUP BY country
ORDER BY total DESC
LIMIT 10;

-- Layoffs by Year
-- Business Question: How did layoffs trend over the years?
SELECT year, SUM(total_laid_off) AS total
FROM layoffs
GROUP BY year
ORDER BY year;

-- Top Companie
-- Business Question: Which companies had the highest total layoffs?
SELECT company, SUM(total_laid_off) AS total
FROM layoffs
GROUP BY company
ORDER BY total DESC
LIMIT 10;

-- Avg Layoff Percentage by Stage
-- Business Question: Which startup stages were most impacted in terms of layoff percentage?
SELECT stage, AVG(percentage_laid_off) AS avg_percentage
FROM layoffs
GROUP BY stage
ORDER BY avg_percentage DESC;