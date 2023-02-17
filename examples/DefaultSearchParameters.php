<?php declare(strict_types=1);


namespace StudyPortals\PageModels\Infrastructure;

use StudyPortals\PageModels\Data\ServiceLayer\Core\IDefaultSearchParameters;

class DefaultSearchParameters implements IDefaultSearchParameters
{
    /**
     * @var ?array<string, array<int, string>|string>
     */
    private $levels;

    /**
     * @return  array<string, array<int, string>|string>
     */
    public function getParameters(): array
    {
        return $this->levels ?? ['levels' => [ 'master']];
    }

    /**
     * @param  array<string, array<int, string>|string>  $levels
     */
    public function setParameters(array $levels): void
    {
        $this->levels = $levels;
    }
}