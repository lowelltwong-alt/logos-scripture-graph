param([Parameter(Mandatory = $true)][string]$ImagePath,[string]$Language = "en-US")
$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Runtime.WindowsRuntime
function Await-WinRtOperation {
    param([Parameter(Mandatory = $true)]$Operation,[Parameter(Mandatory = $true)][Type]$ResultType)
    $method = [System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object { $_.Name -eq "AsTask" -and $_.IsGenericMethod -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq "IAsyncOperation``1" } | Select-Object -First 1
    if (-not $method) { throw "Unable to locate the WinRT AsTask bridge." }
    $task = $method.MakeGenericMethod($ResultType).Invoke($null, @($Operation)); $task.Wait(); return $task.Result
}
$resolved = (Resolve-Path -LiteralPath $ImagePath).Path
$null = [Windows.Storage.StorageFile, Windows.Storage, ContentType = WindowsRuntime]
$null = [Windows.Storage.FileAccessMode, Windows.Storage, ContentType = WindowsRuntime]
$null = [Windows.Graphics.Imaging.BitmapDecoder, Windows.Graphics.Imaging, ContentType = WindowsRuntime]
$null = [Windows.Graphics.Imaging.SoftwareBitmap, Windows.Graphics.Imaging, ContentType = WindowsRuntime]
$null = [Windows.Globalization.Language, Windows.Globalization, ContentType = WindowsRuntime]
$null = [Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType = WindowsRuntime]
$null = [Windows.Media.Ocr.OcrResult, Windows.Foundation, ContentType = WindowsRuntime]
$null = [Windows.Storage.Streams.IRandomAccessStream, Windows.Storage.Streams, ContentType = WindowsRuntime]
$languageObject = [Windows.Globalization.Language]::new($Language)
if (-not [Windows.Media.Ocr.OcrEngine]::IsLanguageSupported($languageObject)) { throw "Windows Media OCR language '$Language' is not installed." }
$engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromLanguage($languageObject)
if ($null -eq $engine) { throw "Windows Media OCR could not create an engine for '$Language'." }
$file = Await-WinRtOperation ([Windows.Storage.StorageFile]::GetFileFromPathAsync($resolved)) ([Windows.Storage.StorageFile])
$stream = Await-WinRtOperation ($file.OpenAsync([Windows.Storage.FileAccessMode]::Read)) ([Windows.Storage.Streams.IRandomAccessStream])
$decoder = Await-WinRtOperation ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)) ([Windows.Graphics.Imaging.BitmapDecoder])
$bitmap = Await-WinRtOperation ($decoder.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
$result = Await-WinRtOperation ($engine.RecognizeAsync($bitmap)) ([Windows.Media.Ocr.OcrResult])
$lines = @(); foreach ($line in $result.Lines) { $words = @(); foreach ($word in $line.Words) { $words += [ordered]@{text=$word.Text;x=[math]::Round($word.BoundingRect.X,3);y=[math]::Round($word.BoundingRect.Y,3);width=[math]::Round($word.BoundingRect.Width,3);height=[math]::Round($word.BoundingRect.Height,3)} }; $lines += [ordered]@{text=$line.Text;words=$words} }
[ordered]@{schema="windows_media_ocr_page_result.v1";language=$engine.RecognizerLanguage.LanguageTag;text_angle=if($null -eq $result.TextAngle){$null}else{[math]::Round([double]$result.TextAngle,6)};text=$result.Text;lines=$lines} | ConvertTo-Json -Depth 8 -Compress
$stream.Dispose(); $bitmap.Dispose()
