<?php

namespace App\Services;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Storage;
use Symfony\Component\Process\Exception\ProcessFailedException;
use Symfony\Component\Process\Process;

class DefectDetectionService
{
    public function processImage(Request $request): ?array
    {
        $script = 'defect.py';

        $pythonScriptPath = base_path('python/' . $script);

        $file = $request->file('file');

        $filePath = $file->storeAs('files', $file->hashName());

        $local = config('app.env') === 'local';

        $command = $local ? ['python3',] : ['sudo', '-u', 'www-data', 'python3',];

        $command[] = $pythonScriptPath;
        $command[] = storage_path('app/public/' . $filePath);

        $process = new Process($command);

        $process->run();

        if (! $process->isSuccessful()) {
            throw new ProcessFailedException($process);
        }

        preg_match('/\{.*\}/', $process->getOutput(), $matches);
        $jsonString = $matches[0];

        $result = json_decode($jsonString, true) ;

        if (! $result) {
            return null;
        }

        $result['image'] = config('app.url') . '/' . $result['image'];

        return [
            'output' => $result,
        ];
    }
}
