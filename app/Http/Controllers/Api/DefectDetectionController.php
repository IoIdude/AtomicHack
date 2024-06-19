<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Services\DefectDetectionService;
use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;
use Illuminate\Support\Facades\Storage;

/**
 * @tags Определение дефекта
 */
class DefectDetectionController extends Controller
{
    public function __construct(private DefectDetectionService $service)
    {
    }

    /**
     * Загрузка изображения сварки
     *
     * @response array{image: string}
     */
    public function uploadImage(Request $request): JsonResource
    {
        $request->validate([
            'file' => 'required|file|max:50000',
        ]);

        return new JsonResource($this->service->processImage($request));
    }
}
