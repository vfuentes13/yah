############### Functions ###############

# scrapes Wikipedia to get the current sp500 ticker list
function getCurrentsp500
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

# gets the content of the previously existing sp500 ticker file
function getLastsp500
{
	# get the file content
	if(!(Test-Path .\sptickers.txt))
	{
		new-item .\sptickers.txt
	} else
	{
		$sp500tickers = get-content .\sptickers.txt
	}
	return $sp500tickers
}

# compares the previous version of the sp500 ticker list with the current one
function compareSp500($previous, $current)
{
	$cmp=(compare-object $previous $current)
	$cmplen=$cmp.length

	if($cmplen -gt 0)
	{
		$in = @()
		$out = @()
		$res = @{}
		$i=0		
		while($i -lt $cmplen)
		{
			if($cmp[$i].SideIndicator -eq "=>"){
				$in += $cmp[$i].inputObject	
			} 
			elseif($cmp[$i].SideIndicator -eq "<="){
				$out += $cmp[$i].inputObject
			}
			$i+=1
		}
	}
	$res.in_=$in
	$res.out_=$out
	return $res
}

# updates flat file with all the current sp500 tickers
function updateList($switchList)
{
	$max = ($switchList['in_'].length,$switchList['out_'].length | Measure -Max).Maximum
	for($i -eq 0 ; $i -le $max ; $i++){
		get-content .\sptickers.txt | select-string -pattern $switchList['out_'][$i] -notmatch | Out-File .\sptickers.txt
		Add-Content .\sptickers.txt $switchList['in_'][$i]

	}
}


############################################# MAIN #############################################

$curr = getCurrentsp500

if(!(Test-Path .\sptickers.txt))
{
	new-item .\sptickers.txt
	$curr > .\sptickers.txt
}

$prev = getLastsp500
$switch = comparesp500 $prev $curr

updateList $switchList










