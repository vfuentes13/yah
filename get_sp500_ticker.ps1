function get-sp500
{
	# getting data from wikipedia page source code and extracting the lines we are interested in
	$res = invoke-webrequest https://en.wikipedia.org/wiki/List_of_S%26P_500_companies
	$html = $res.parsedHtml.getElementsByTagName('tr') 
	$tags = $html | select InnerHTML
	
	# declaring result array and iteration variable
	$sp500tickers=@()
	$i=0
	
	# looping through all the lines and extracting the ticker
	while(1)
	{
		$line=($tags[$i].innerHTML -split '\n')[0]	
		$ticker=$line.split('>')[2].split('<')[0]
		if($ticker -match "^[A-Z+]")
		{
			$sp500tickers+=$ticker
		}
		else
		{
			break
		}
		$i+=1	
	}
	return $sp500tickers
}

$currentList = get-sp500
if(!(Test-Path .\sptickers.txt))
{
	new-item .\sptickers.txt
} else
{
	#$currentFile = get-item .\sptickers.txt
	$currentFile = get-content .\sptickers.txt
}

if((compare-object $currentFile $currentList).length>0)
{
	# update the file that has side indicator :: =>
}

